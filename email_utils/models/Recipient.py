# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

BLACKLIST_RECIPIENT_PERMISSION = 'can_blacklist_recipient'
WHITELIST_RECIPIENT_PERMISSION = 'can_whitelist_recipient'


@python_2_unicode_compatible
class Recipient(models.Model):
    BLACKLIST_RECIPIENT_PERMISSION = BLACKLIST_RECIPIENT_PERMISSION
    WHITELIST_RECIPIENT_PERMISSION = WHITELIST_RECIPIENT_PERMISSION

    address = models.CharField(max_length=256)
    nonce = models.CharField(max_length=64, blank=True)
    blacklist = models.BooleanField(default=False)

    class Meta:
        app_label = 'email_utils'
        verbose_name = _('Recipient')
        verbose_name_plural = _('Recipients')
        permissions = [
            (BLACKLIST_RECIPIENT_PERMISSION, _('Can blacklist recipients')),
            (WHITELIST_RECIPIENT_PERMISSION, _('Can whitelist recipients'))
        ]

    def __str__(self):
        return self.address
