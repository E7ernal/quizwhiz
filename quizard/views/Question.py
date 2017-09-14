# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.http import Http404, JsonResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.db.models import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse

from quizard.models import Assignment


class Question(generic.View):
    def dispatch(self, request, *pos, **kw):
        assignment = get_object_or_404(Assignment, code=kw['code'])

        try:
            question = assignment.get_question_by_slug(kw['question_slug'])
        except ObjectDoesNotExist:
            raise Http404()

        return super(Question, self).dispatch(
            request,
            assignment=assignment,
            question=question
        )

    def get(self, request, assignment, question):
        # Update the user's position within this assignment.
        request.session['assignment_in_progress'] = request.get_full_path()

        if question.pk not in request.session['visited_questions']:
            # Sessions are only saved when the session object is modified.
            # Appending something to a value in the session dict modifies
            # that value, not the session itself.
            request.session.modified = True
            request.session['visited_questions'].append(question.pk)

        total_questions = assignment.num_questions
        completed_questions = max(0, len(request.session['visited_questions']) - 1)
        percent = (completed_questions / float(total_questions)) * 100.0

        context = {
            'question': question,
            'percent_done': "{percent:0.0f}".format(percent=percent),
            'total_questions': total_questions,
            'completed_questions': completed_questions
        }

        return TemplateResponse(request, 'quizard/question.html', context)

    def post(self, request, assignment, question):
        """
        Records the given answer and redirects to the next question.
        The next question is randomly determined.
        """
        request.session.modified = True

        request.session['answers'][question.pk] = request.POST['answer']

        try:
            next_question = assignment.get_random_question(request.session['visited_questions'])
        except Assignment.OutOfQuestions:
            next_url = reverse('results', kwargs={'code': assignment.code})

            # If this was the last question, the assignment has been
            # completed, so we can stop tracking their position.
            del request.session['assignment_in_progress']
            request.session.modified = True
        else:
            next_url = reverse('question', kwargs={
                'code': assignment.code,
                'question_slug': next_question.slug
            })

        return JsonResponse({
            'status': 200,
            'correct_answer': None,
            'next_url': next_url
        })
