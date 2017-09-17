# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.contrib.admin import ModelAdmin
from django.utils.translation import ugettext_lazy as _


class AbstractBaseAdmin(ModelAdmin):
    readonly_fields = ['created_by', 'created', 'last_modified']

    fieldsets = [
        (_('Meta information'), {
            'fields': ['created_by', 'created', 'last_modified'],
            'classes': ['collapse']
        })
    ]

    def save_model(self, request, obj, form, change):
        """
        Populate AbstractBase.created_by with the user who
        submitted the request.
        """
        if not change:
            obj.created_by = request.user
        return super(AbstractBaseAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """
        Populate AbstractBase.created_by on inlined relations
        with the user who submitted the request.
        """
        for form in formset.extra_forms:
            if form.has_changed:
                form.instance.created_by = request.user
        return super(AbstractBaseAdmin, self).save_formset(request, form, formset, change)


