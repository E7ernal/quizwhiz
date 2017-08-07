# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from quizard.models import Assignment, AssignmentQuestion

from AbstractBaseAdmin import AbstractBaseAdmin


class AssignmentQuestionInline(admin.TabularInline):
    model = AssignmentQuestion
    extra = 0
    min_num = 0

    fields = ['index', 'question_type', 'question_id']


class AssignmentAdmin(AbstractBaseAdmin):
    inlines = [AssignmentQuestionInline]

    save_as = True

    search_fields = ['name', 'school__name', 'code']
    list_filter = ['school__name', 'is_private', 'created', 'created_by__username']

    list_display = [
        'name', 'code', 'school', 'num_questions',
        'is_private', 'created_by', 'created'
    ]

    fieldsets = [
        (_('Assignment configuration'), {
            'fields': ['school', 'name', 'code', 'is_private']
        }),
        (_('About this assignment'), {
            'fields': ['summary', 'description']
        })
    ] + AbstractBaseAdmin.fieldsets
