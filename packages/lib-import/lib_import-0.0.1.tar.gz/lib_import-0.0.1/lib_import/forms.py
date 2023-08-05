from django import forms
from django.utils.translation import gettext as _


class ImportForm(forms.Form):
    """Form with mandatory fields to make import."""

    import_file = forms.fields.FileField(
        label=_('label_import_file')
    )
    import_type = forms.fields.ChoiceField(
        choices=[
            ('create_only', _('choice_import_create_only')),
            ('create_update', _('choice_import_create_update'))
        ],
        widget=forms.RadioSelect,
        label=_('label_import_type')
    )
