# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.views import generic

from NavLocationMixin import NavLocationMixin


class About(NavLocationMixin, generic.TemplateView):
    location = 'about'
    template_name = 'quizard/about.html'
