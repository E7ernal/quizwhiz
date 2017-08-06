# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractBase(models.Model):
    created_by = models.ForeignKey('auth.User', verbose_name=_('Created by'))

    created = models.DateTimeField(_('Created on'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    class Meta:
        app_label = 'quizard'
        abstract = True
