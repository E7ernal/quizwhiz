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

    def post(self, request, *pos, **kw):
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kw):
        context = super(Assignment, self).get_context_data(**kw)

        context['form'] = self.get_form()

        # Get the user's score for this assignment, if it exists.
        completed_assignments = self.request.session.get('completed_assignments', {})
        context['score'] = completed_assignments.get(self.object.code, None)

        self.initialize_session(context['assignment'])

        return context

    def initialize_session(self, assignment):
        """
        Initialize the user's assignment-taking session. We record
        - The current assignment's code.
        - The user's position within the assignment (in the form of a URL).
        - A list of questions the user has visited.
        - A dict of question-answer pairs the users has submitted.
        """
        self.request.session['assignment_code'] = assignment.code
        self.request.session['assignment_in_progress'] = self.request.get_full_path()
        self.request.session['visited_questions'] = []
        self.request.session['answers'] = {}

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
