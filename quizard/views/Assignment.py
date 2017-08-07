# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.views import generic

from quizard import models


class Assignment(generic.DetailView):
    model = models.Assignment
    slug_field = 'code'
    slug_url_kwarg = 'code'
    context_object_name = 'assignment'
    template_name = 'quizard/assignment.html'
