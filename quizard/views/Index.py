# vim: ts=4:sw=4:expandtabs

__authors__ = "Zach Mott, David Fox, Jason Dunn"

from django.views import generic
from django.shortcuts import redirect

from quizard.forms import AssignmentSearchForm

from NavLocationMixin import NavLocationMixin


class Index(NavLocationMixin, generic.FormView):
    location = 'index'
    form_class = AssignmentSearchForm
    template_name = 'quizard/index.html'

    def form_valid(self, form):
        code = form.cleaned_data.get('code', None)
        school = form.cleaned_data.get('school', None)
        teacher = form.cleaned_data.get('teacher', None)

        if code:
            return redirect('assignment', code=code)
        elif school and teacher:
            return redirect('assignments', school=school, teacher=teacher)
        else:
            return redirect('index')
