# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.views import generic
from django.core.urlresolvers import reverse

from quizard import models
from quizard.forms import AssignmentStartForm


class Assignment(generic.edit.FormMixin, generic.DetailView):
    model = models.Assignment
    slug_field = 'code'
    slug_url_kwarg = 'code'
    context_object_name = 'assignment'
    template_name = 'quizard/assignment.html'
    form_class = AssignmentStartForm

    def get_context_data(self, **kw):
        context = super(Assignment, self).get_context_data(**kw)

        context['form'] = self.get_form()
        self.initialize_session(context['assignment'])

        context['question_slug'] = context['assignment'].get_random_question().slug
        return context

    def initialize_session(self, assignment):
        self.request.session['assignment_code'] = assignment.code
        self.request.session['visited_questions'] = []
        self.request.session['answers'] = {}

    def post(self, request, *pos, **kw):
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.request.session['assignee_name'] = form.cleaned_data['name']
        self.request.session['assignee_email'] = form.cleaned_data['email']
        return super(Assignment, self).form_valid(form)

    def get_success_url(self):
        return reverse('question', kwargs={
                'code': self.object.code,
                'question_slug': self.object.get_random_question().slug
            }
        )
