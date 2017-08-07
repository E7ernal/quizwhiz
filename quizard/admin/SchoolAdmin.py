# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.utils.translation import ugettext_lazy as _

from quizard.models import School
from quizard.admin.AbstractBaseAdmin import AbstractBaseAdmin


class SchoolAdmin(AbstractBaseAdmin):
    search_fields = ['name']

    fieldsets = [
        (None, {
            'fields': ['name']
        })
    ] + AbstractBaseAdmin.fieldsets
