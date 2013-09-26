from django import forms
from django.conf import settings
from django.utils.encoding import force_unicode

OTHER_CHOICE = ''

class ChoiceWithOtherWidget(forms.MultiWidget):
    """MultiWidget for use with ChoiceWithOtherField."""
    def __init__(self, choices, attrs=None):
        widgets = [
            forms.Select(choices=choices),
            forms.TextInput(attrs={'size':'80'})
        ]
        self.choices = choices
        super(ChoiceWithOtherWidget, self).__init__(widgets, attrs=attrs)

    def decompress(self, value):
        if value:
            choices = [c[0] for c in self.choices]
            provided_choices, other_choice = choices[:-1], choices[-1:]
            if value in provided_choices:
                return [value, '']
            else:
                return [OTHER_CHOICE, value]
        return ['', '']

    def format_output(self, rendered_widgets):
        """Format the output by substituting the "other" choice into the first widget."""
        return '<div class="choice_with_other_wrapper">%s %s</div>' % \
            (rendered_widgets[0], rendered_widgets[1])

    def _media(self):
        js_list = ['%sadmin/choice_with_other.js' % settings.STATIC_URL, ]
        return forms.Media(js=js_list)
    media = property(_media)


class ChoiceWithOtherField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        choices = list(kwargs.pop('choices'))
        has_empty_choice = False
        for c in choices:
            if not c[0]:
                has_empty_choice = True
                break
        if not has_empty_choice:
            choices.insert(0, ('', '---------'))
        #choices.append((OTHER_CHOICE, 'Other: '))
        fields = [
            forms.ChoiceField(choices=choices),
            forms.CharField(required=False)
        ]
        widget = ChoiceWithOtherWidget(choices=choices)
        self._was_required = kwargs.pop('required', True)
        kwargs['required'] = False
        super(ChoiceWithOtherField, self).__init__(widget=widget, fields=fields, *args, **kwargs)

    def compress(self, value):
        if self._was_required and (not value or value[0] in (None, '')):
            raise forms.ValidationError(self.error_messages['required'])
        if not value:
            return ''

        if force_unicode(value[0]) == OTHER_CHOICE:
            return value[1]
        else:
            return value[0]

