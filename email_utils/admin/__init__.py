# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.contrib import admin

from EmailMessageAdmin import EmailMessage, EmailMessageAdmin
from RecipientAdmin import Recipient, RecipientAdmin

admin.site.register(EmailMessage, EmailMessageAdmin)
admin.site.register(Recipient, RecipientAdmin)
