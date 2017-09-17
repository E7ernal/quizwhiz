# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _

from email_utils.models import Recipient


class RecipientAdmin(admin.ModelAdmin):
    search_fields = ['address', 'nonce']

    list_display = ['address', 'blacklist']
    list_filter = ['blacklist']

    actions = ['blacklist_recipients', 'whitelist_recipients']

    fieldsets = [
        (None, {
            'fields': ['address', 'blacklist'],
        }),
        (_('Nonce'), {
            'fields': ['nonce'],
            'classes': ['collapse']
        })
    ]

    def get_actions(self, request):
        actions = super(RecipientAdmin, self).get_actions(request)

        if not request.user.has_perm(Recipient.BLACKLIST_RECIPIENT_PERMISSION):
            del actions['blacklist_recipients']
        if not request.user.has_perm(Recipient.WHITELIST_RECIPIENT_PERMISSION):
            del actions['whitelist_recipients']

        return actions

    def blacklist_recipients(self, request, queryset):
        queryset.update(blacklist=True)
        messages.info(request, "Blacklisted {count} recipients.".format(
            count=queryset.count()
        ))
    blacklist_recipients.short_description = _('Blacklist selected recipients')

    def whitelist_recipients(self, request, queryset):
        queryset.update(blacklist=False)
        messages.info(request, "Whitelisted {count} recipients.".format(
            count=queryset.count()
        ))
    whitelist_recipients.short_description = _('Whitelist selected recipients')
