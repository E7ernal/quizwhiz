# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from django.contrib import admin

from quizard.admin.mixins.ViewOnlyMixin import ViewOnlyMixin

from AssignmentAdmin import Assignment, AssignmentAdmin
from FreeResponseQuestionAdmin import FreeResponseQuestion, FreeResponseQuestionAdmin
from MultipleChoiceQuestionAdmin import MultipleChoiceQuestion, MultipleChoiceQuestionAdmin
from SchoolAdmin import School, SchoolAdmin


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(FreeResponseQuestion, FreeResponseQuestionAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(School, SchoolAdmin)
