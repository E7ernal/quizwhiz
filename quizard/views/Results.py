# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.views import generic
from django.shortcuts import redirect

from quizard.models.Assignment import Assignment


class Results(generic.TemplateView):
    template_name = 'quizard/results.html'

    def get(self, request, *pos, **kw):
        # If the user isn't currently working on an assignment,
        # they shouldn't be allowed to access the results page.
        if 'assignment_code' not in self.request.session:
            return redirect('index')
        return super(Results, self).get(request, *pos, **kw)

    def get_context_data(self, **kw):
        context = super(Results, self).get_context_data(**kw)

        context['assignment'] = Assignment.objects.get(code=self.kwargs['code'])
        context['questions'] = self.build_question_dicts(
            context['assignment'],
            self.request.session['answers']
        )

#        del self.request.session['assignment_code']
#        self.request.session.modified = True

        return context

    def build_question_dicts(self, assignment, answers):
        question_list = []

        print answers

        for question in assignment.questions.all():
            question_list.append({
                'question': question,
                'answer': answers[str(question.pk)],
                'correct': question.validate_answer(answers[str(question.pk)]),
            })

        return question_list