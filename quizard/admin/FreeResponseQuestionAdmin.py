# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from django.contrib import admin

from quizard.admin import ViewOnlyMixin
from quizard.models import FreeResponseAnswer, FreeResponseQuestion

from AbstractBaseAdmin import AbstractBaseAdmin


class FreeResponseAnswerInline(ViewOnlyMixin, admin.TabularInline):
    model = FreeResponseAnswer
    extra = 0
    min_num = 0

    fields = ['value']


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


