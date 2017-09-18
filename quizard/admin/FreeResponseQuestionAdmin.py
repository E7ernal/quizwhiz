# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from quizard.admin import ViewOnlyMixin
from quizard.models import FreeResponseAnswer, FreeResponseQuestion

from AbstractBaseAdmin import AbstractBaseAdmin


class FreeResponseAnswerFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        clean_result = super(FreeResponseAnswerFormset, self).clean()

        value_list = [form.cleaned_data['value'].lower() for form in self.forms]
        value_set = set(value_list)

        # If there are fewer items in the value set than there are in
        # the value list, some of the answers were duplicated.
        if len(value_set) < len(value_list):
            raise forms.ValidationError(_('Answer values must be unique '
                                          'on a case-insensitive basis.'))

        return clean_result


class FreeResponseAnswerInline(ViewOnlyMixin, admin.TabularInline):
    model = FreeResponseAnswer
    formset = FreeResponseAnswerFormset
    extra = 0
    min_num = 0

    fields = ['value', 'case_sensitive']
    prepopulated_fields = {}  # Prevents inline from using its parent's prepopulated_fields.


class FreeResponseQuestionAdmin(ViewOnlyMixin, AbstractBaseAdmin):
    inlines = [FreeResponseAnswerInline]

    list_filter = ['created']
    list_display = ['title', 'created_by', 'point_value']
    search_fields = ['title']

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'point_value', 'html', 'explanation']
        })
    ] + AbstractBaseAdmin.fieldsets

    def get_prepopulated_fields(self, request, obj=None):
        supercall = super(FreeResponseQuestionAdmin, self).get_prepopulated_fields
        prepopulated_fields = supercall(request, obj=obj)

        if request.user.is_superuser or (obj and obj.created_by == request.user):
            prepopulated_fields['slug'] = ('title',)

        return prepopulated_fields


