# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from email_utils.tasks import send_mail

RESEND_EMAIL_PERMISSION = 'can_resend_email'


class EmailMessage(models.Model):
    RESEND_EMAIL_PERMISSION = RESEND_EMAIL_PERMISSION

    to = models.CharField(max_length=256)
    from_address = models.CharField(max_length=256, verbose_name=_('From'))
    subject = models.CharField(max_length=256, blank=True)
    body = models.TextField()
    html_body = models.TextField(blank=True, verbose_name=_('HTML body'))

    date_sent = models.DateTimeField()

    delivery_successful = models.BooleanField()
    error_message = models.CharField(max_length=256, blank=True)

    class Meta:
        app_label = 'email_utils'
        verbose_name = _('Email message')
        verbose_name_plural = _('Email messages')
        permissions = [
            (RESEND_EMAIL_PERMISSION, _('Can resend email')),
        ]

    def resend(self):
        send_mail.apply_async((
            self.subject,
            self.body,
            self.from_address,
            self.to
        ), {'html_message': self.html_body})
