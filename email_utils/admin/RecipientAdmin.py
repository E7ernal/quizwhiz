# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from email_utils.models import Recipient


class RecipientAdmin(admin.ModelAdmin):
    pass