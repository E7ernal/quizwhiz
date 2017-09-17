# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from quizard.admin import ViewOnlyMixin
from quizard.models import MultipleChoiceAnswer, MultipleChoiceQuestion

from AbstractBaseAdmin import AbstractBaseAdmin


class MultipleChoiceAnswerInline(ViewOnlyMixin, admin.TabularInline):
    model = MultipleChoiceAnswer
    fields = ['is_correct', 'value']
    extra = 0
    min_num = 0


class MultipleChoiceQuestionAdmin(ViewOnlyMixin, AbstractBaseAdmin):
    inlines = [MultipleChoiceAnswerInline]

    list_filter = ['created']
    list_display = ['title', 'created_by', 'point_value']
    search_fields = ['title']

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'point_value', 'html', 'explanation']
        })
    ] + AbstractBaseAdmin.fieldsets

    def get_prepopulated_fields(self, request, obj=None):
        supercall = super(MultipleChoiceQuestionAdmin, self).get_prepopulated_fields
        prepopulated_fields = supercall(request, obj=obj)

        if request.user.is_superuser or (obj and obj.created_by == request.user):
            prepopulated_fields['slug'] = ('title',)

        return prepopulated_fields
