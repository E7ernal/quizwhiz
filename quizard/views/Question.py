# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.views import generic
from django.template.response import TemplateResponse

from quizard.models import Assignment


class Question(generic.View):
    def get(self, request, code, question_slug=None):
        assignment = Assignment.objects.get(code=code)

        if request.session.get('assignment_code', '') != assignment.code:
            request.session['assignment_code'] = assignment.code
            request.session['visited_questions'] = []

        question = assignment.get_question(question_slug, request.session['visited_questions'])
        request.session['visited_questions'].append(question.pk)

        return TemplateResponse(
            request,
            'quizard/question.html',
            {'question': question}
        )

    def post(self, request, code, question_slug=None):
        return TemplateResponse(
            request,
            'quizard/question_explanation.html',
            {}
        )


