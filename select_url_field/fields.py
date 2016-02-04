import re

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from select_url_field import select_url_field_settings

try:
    from importlib import import_module
except ImportError:
    # Django < 1.9 and Python < 2.7
    from django.utils.importlib import import_module


from select_url_field.choice_with_other import ChoiceWithOtherField


class SelectURLField(models.CharField):
    description = _("URL")

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 200)
        # Handle choices option:
        # from custom_site.url_choices import get_url_choices
        # link = SelectURLField(blank=True, choices=get_url_choices)
        self._has_choices = False
        if 'choices' in kwargs:
            self._has_choices = True
            self._url_choices = kwargs.pop('choices')
        
        models.CharField.__init__(self, verbose_name, name, **kwargs)
        self.validators.append(SelectURLValidator())

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed twice
        defaults = {
            'form_class': SelectURLFormField,
        }
        defaults.update(kwargs)
        # When choices given, use them
        # When not, use global settings
        if self._has_choices:
            if callable(self._url_choices):
                choices = self._url_choices()
            else:
                choices = self._url_choices
        else:
            mod_path, func_name = select_url_field_settings.URL_CHOICES_FUNC.rsplit('.', 1)
            mod = import_module(mod_path)
            choices_func = getattr(mod, func_name)
            choices = choices_func()
        required = not self.blank
        return ChoiceWithOtherField(choices=choices, required=required)

    def to_python(self, value):
        from django.conf import settings
        if value:
            domain = getattr(settings, 'SITE_DOMAIN', '')
            if domain:
                domain_pattern = r'^(?:http|ftp)s?://' + domain
                domain_regex = re.compile(domain_pattern, re.IGNORECASE)
                value = domain_regex.sub('', value)
        return super(SelectURLField, self).to_python(value)


# We need IxxyURLField so this is backwards compatible
IxxyURLField = SelectURLField


class SelectURLValidator(object):
    
    code = 'invalid'
    regex = re.compile(r'(?:[/?]\S+)$', re.IGNORECASE)

    def __init__(self):
        self.url_validator = URLValidator()
        
    def __call__(self, value):
        try:
            # OK if it's a valid url
            self.url_validator(value)
        except ValidationError, e:
            # Not a valid url, see it's a path
            if not self.regex.search(smart_unicode(value)):
                raise e


class SelectURLFormField(forms.CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid URL.'),
    }

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(SelectURLFormField, self).__init__(max_length, min_length, *args, **kwargs)
        self.validators.append(SelectURLValidator())


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^select_url_field\.fields\.IxxyURLField"])
    add_introspection_rules([], ["^select_url_field\.fields\.SelectURLField"])
