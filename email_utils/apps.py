# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmailUtilsConfig(AppConfig):
    name = 'email_utils'
    verbose_name = _('Email')
