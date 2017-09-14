# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.conf import settings
from django.views import generic
from django.shortcuts import redirect
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from quizard.utils import send_mail
from quizard.models.Assignment import Assignment


class Results(generic.DetailView):
    model = Assignment
    slug_field = 'code'
    slug_url_kwarg = 'code'
    context_object_name = 'assignment'
    template_name = 'quizard/results.html'

    def get(self, request, *pos, **kw):
        # If the user isn't currently working on an assignment,
        # they shouldn't be allowed to access the results page.
        if 'assignment_code' not in self.request.session:
            return redirect('index')
        return super(Results, self).get(request, *pos, **kw)

    def get_context_data(self, **kw):
        context = super(Results, self).get_context_data(**kw)

        context['questions'] = self.build_question_dicts(
            context['assignment'],
            self.request.session['answers']
        )
        context['points_earned'] = self.calculate_points_earned(context['questions'])

        try:
            self.request.session['completed_assignments'].append(self.object.code)
        except KeyError:
            self.request.session['completed_assignments'] = [self.object.code]
#        del self.request.session['assignment_code']
#        self.request.session.modified = True

        self.send_emails()

        return context

    def build_question_dicts(self, assignment, answers):
        question_list = []

        for question in assignment.questions.all():
            question_list.append({
                'question': question,
                'answer': answers[str(question.pk)],
                'correct': question.validate_answer(answers[str(question.pk)]),
            })

        return question_list

    def calculate_points_earned(self, question_dict):
        return reduce(lambda x, y: x + y, [q['question'].point_value for q in question_dict if q['correct']])

    def send_emails(self):
        self.send_teacher_email(self.object)
        self.send_summary_email(self.object)

    def send_teacher_email(self, assignment):
        """
        Email the assignment creator the results of this particular
        quiz-taking session.
        """
        self._send_email(
            assignment,
            assignment.created_by.email,
            'quizard/emails/assignment_results.txt'
        )

    def send_summary_email(self, assignment):
        """
        Sent a results receipt to the given third-party, if there is one.
        """
        if self.request.session.get('assignee_email', None):
            self._send_email(
                assignment,
                self.request.session['assignee_email'],
                'quizard/emails/assignment_results_summary.txt'
            )

    def _send_email(self, assignment, to_address, email_template):
        template_instance = get_template(email_template)
        context = {
            'assignment': assignment,
            'questions': self.build_question_dicts(
                assignment,
                self.request.session['answers'],
            ),
            'assignee_name': self.request.session['assignee_name'],
            'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
            'BRAND_NAME': settings.BRAND_NAME
        }

        context['points_earned'] = self.calculate_points_earned(context['questions'])

        subject = _("{assignment.code} results -- {assignee_name}").format(**context)

        # Make a bona fide attempt to figure out who this email
        # is supposed to go to.
        if isinstance(to_address, list) or isinstance(to_address, tuple):
            to_address_list = to_address
        else:
            try:
                to_address_list = to_address.split(',')
            except AttributeError:
                return None

        return send_mail(
            subject,
            template_instance.render(context),
            settings.DEFAULT_FROM_EMAIL,
            to_address_list
        )


