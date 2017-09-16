# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _

from email_utils.models import EmailMessage


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'to', 'from_address', 'delivery_successful', 'date_sent']
    list_filter = ['delivery_successful', 'date_sent']

    actions = ['resend_emails']

    fieldsets = [
        (None, {
            'fields': ['to', 'from_address', 'subject']
        }),
        (_('Body'), {
            'fields': ['body', 'html_body'],
            'classes': ['collapse'],
        }),
        (_('Delivery information'), {
            'fields': ['date_sent', 'delivery_successful', 'error_message']
        })
    ]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(EmailMessageAdmin, self).get_readonly_fields(request, obj=obj)

        if not request.user.is_superuser:
            readonly_fields.append([
                'to', 'from_address', 'subject', 'body', 'html_body',
                'date_sent', 'delivery_successful', 'error_message',
            ])

        return readonly_fields

    def get_actions(self, request):
        actions = super(EmailMessageAdmin, self).get_actions(request)

        if not request.user.has_perm(EmailMessage.RESEND_EMAIL_PERMISSION):
            del actions['resend_email']

        return actions

    def resend_emails(self, request, queryset):
        for emailmessage in queryset:
            emailmessage.resend()
        messages.info(request, _('{count} emails resent.').format(count=queryset.count()))
    resend_emails.short_description = _('Resend selected emails')
