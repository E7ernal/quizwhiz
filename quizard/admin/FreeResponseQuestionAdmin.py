# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from quizard.models import FreeResponseAnswer, FreeResponseQuestion

from AbstractBaseAdmin import AbstractBaseAdmin


class FreeResponseAnswerInline(admin.TabularInline):
    model = FreeResponseAnswer
    extra = 0
    min_num = 0

    fields = ['value']


class FreeResponseQuestionAdmin(AbstractBaseAdmin):
    inlines = [FreeResponseAnswerInline]

    list_filter = ['created']
    list_display = ['title', 'created_by', 'point_value']
    search_fields = ['title']

    fieldsets = [
        (None, {
            'fields': ['title', 'point_value', 'html', 'explanation']
        })
    ] + AbstractBaseAdmin.fieldsets


