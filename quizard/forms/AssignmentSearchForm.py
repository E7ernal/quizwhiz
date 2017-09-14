# vim: ts=4:sw=4:expandtabs

__authors__ = "Zach Mott, David Fox, Jason Dunn"

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class AssignmentSearchForm(forms.Form):
    INVALID_INPUT_COMBO_MSG = _('Please provide an assignment code or '
                                'a teacher and a school, but not both.')

    school = forms.CharField(max_length=64, required=False)
    teacher = forms.CharField(
        max_length=64,
        required=False,
        help_text=_("Your teacher's last name.")
    )
    code = forms.CharField(max_length=16, required=False)

    def clean(self):
        cleaned_data = super(AssignmentSearchForm, self).clean()

        teacher = cleaned_data['teacher']
        school = cleaned_data['school']
        code = cleaned_data['code']

        if all([teacher, school, code]) or not any([teacher, school, code]):
            raise ValidationError(self.INVALID_INPUT_COMBO_MSG)

        return cleaned_data
