import re
import os.path

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.cache import cache
from django.db import models
from django.db import IntegrityError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

from ixxy_url_field.choice_with_other import ChoiceWithOtherField

class IxxyURLField(models.CharField):
    description = _("URL")

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 200)
        models.CharField.__init__(self, verbose_name, name, **kwargs)
        self.validators.append(IxxyURLValidator())

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed twice
        defaults = {
            'form_class': IxxyURLFormField,
        }
        defaults.update(kwargs)
        cache_key = 'get_linklist_context'
        linklists = cache.get(cache_key)
        if not linklists:
            from cms.admin_views import get_linklist_context
            linklists = get_linklist_context()
            cache.set(cache_key, linklists)
        choices = []
        keys = ['links', 'documents', 'secure_documents', ]
        for key in keys:
            choices.extend([(link[1], link[0]) for link in linklists[key] or []])
            choices.append(['', ''])
        
        required = not self.blank
        return ChoiceWithOtherField(choices=choices, required=required)


    def to_python(self, value):
        from django.conf import settings
        if value:
            domain = getattr(settings, 'SITE_DOMAIN', '')
            if domain:
                domain_pattern = r'^(?:http|ftp)s?://' + domain
                domain_regex = re.compile(domain_pattern, re.IGNORECASE)
                #match = domain_regex.search(value)
                value = domain_regex.sub('', value)
        return super(IxxyURLField, self).to_python(value)



class IxxyURLValidator(object):
    code = 'invalid'
    regex = re.compile(r'(?:[/?]\S+)$', re.IGNORECASE)

    def __init__(self):
        self.url_validator = URLValidator()
        
    def __call__(self, value):
        try:
            #OK if it's a valid url 
            self.url_validator(value)
        except ValidationError, e:
            #Not a valid url, see it's a path 
            if not self.regex.search(smart_unicode(value)):
                raise e

class IxxyURLFormField(forms.CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid URL.'),
    }

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(IxxyURLFormField, self).__init__(max_length, min_length, *args, **kwargs)
        self.validators.append(IxxyURLValidator())

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^ixxy_url_field\.fields\.IxxyURLField"])