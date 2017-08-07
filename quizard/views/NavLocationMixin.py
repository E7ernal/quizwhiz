# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


class NavLocationMixin(object):
    location = None

    def get_context_data(self, **kw):
        context = super(NavLocationMixin, self).get_context_data(**kw)
        context['location'] = self.location
        return context
