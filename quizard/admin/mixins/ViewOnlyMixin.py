# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.core.urlresolvers import resolve


class ViewOnlyMixin(object):
    def get_parent_instance_from_request(self, request):
        """
        Thanks, https://stackoverflow.com/questions/32150088/!
        """
        resolved = resolve(request.path_info)
        if resolved.args and getattr(self, 'parent_model', None):
            return self.parent_model.objects.get(pk=resolved.args[0])
        return None

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(ViewOnlyMixin, self).get_readonly_fields(
            request,
            obj=obj
        ))

        if request.user.is_superuser:
            return readonly_fields

        if obj is not None and obj.created_by != request.user:
            readonly_fields.extend(self.get_view_only_fields(request, obj=obj))

        return readonly_fields

    def get_view_only_fields(self, request, obj=None):
        fields = []

        if getattr(self, 'view_only_fields', None):
            fields = self.view_only_fields
        if getattr(self, 'fields', None):
            fields = self.fields
        if getattr(self, 'fieldsets', None):
            fields = []
            for _, dict_ in self.fieldsets:
                fields.extend(dict_['fields'])

        return fields

    def has_add_permission(self, request):
        add_permission = super(ViewOnlyMixin, self).has_add_permission(request)

        parent_instance = self.get_parent_instance_from_request(request)

        if request.user.is_superuser or parent_instance is None:
            return add_permission

        if parent_instance.created_by != request.user:
            add_permission &= False

        return add_permission

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.created_by == request.user)
