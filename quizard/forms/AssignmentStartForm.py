# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class AssignmentStartForm(forms.Form):
    name = forms.CharField(max_length=256)
    confirm_name = forms.CharField(
        max_length=256,
        help_text=_('Please confirm your name.')
    )
    email = forms.EmailField(
        required=False,
        help_text=_('Optional: Enter your email address to '
                    'receive a copy of your assignment results.')
    )

    def clean(self):
        cleaned_data = super(AssignmentStartForm, self).clean()

        if cleaned_data['name'] != cleaned_data['confirm_name']:
            raise ValidationError(_("'Name' and 'Confirm name' fields "
                                    "must contain the same value."))

        return cleaned_data