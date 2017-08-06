# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from quizard.models.BaseQuestion import BaseQuestion


class FreeResponseQuestion(BaseQuestion):
    class Meta:
        verbose_name = _('Free response question')
        verbose_name_plural = _('Free response questions')
