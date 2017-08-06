# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from quizard.models import MultipleChoiceAnswer, MultipleChoiceQuestion

from AbstractBaseAdmin import AbstractBaseAdmin


class MultipleChoiceAnswerInline(admin.TabularInline):
    model = MultipleChoiceAnswer
    fields = ['is_correct', 'value']
    extra = 0
    min_num = 0


class MultipleChoiceQuestionAdmin(AbstractBaseAdmin):
    inlines = [MultipleChoiceAnswerInline]

    list_filter = ['created']

    list_display = ['__str__', 'point_value']

    fieldsets = [
        (None, {
            'fields': ['point_value', 'html', 'explanation']
        })
    ] + AbstractBaseAdmin.fieldsets
