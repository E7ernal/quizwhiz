# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Recipient(models.Model):
    address = models.CharField(max_length=256)
    nonce = models.CharField(max_length=64, blank=True)
    blacklist = models.BooleanField(default=False)

    class Meta:
        app_label = 'email_utils'
        verbose_name = _('Recipient')
        verbose_name_plural = _('Recipients')
