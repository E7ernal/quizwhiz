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

    def get_context_data(self, **kw):
        context = super(Assignment, self).get_context_data(**kw)

        self.initialize_session(context['assignment'])

        context['question_slug'] = context['assignment'].get_random_question().slug
        return context

    def initialize_session(self, assignment):
        self.request.session['assignment_code'] = assignment.code
        self.request.session['visited_questions'] = []
        self.request.session['answers'] = {}
