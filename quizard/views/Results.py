# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.conf import settings
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from email_utils.tasks import send_mail
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
            messages.info(request, _('You must complete an assignment before visiting the results page.'))
            return redirect('index')

        # If the assignment is still in progress (i.e., we have a current position),
        # send the user back to that position rather than allowing them to view their
        # (incomplete) results.
        if isinstance(request.session.get('assignment_in_progress', None), basestring):
            messages.info(request, _('You must complete this assignment before viewing your results.'))
            return redirect(request.session['assignment_in_progress'])

        return super(Results, self).get(request, *pos, **kw)

    def get_context_data(self, **kw):
        context = super(Results, self).get_context_data(**kw)

        context.update({
            'points_earned': self.object.calculate_score(self.request.session['answers']),
            'questions': self.build_question_dicts(
                context['assignment'],
                self.request.session['answers']
            )
        })

        # Record the user's score on this assignment.
        completed_assignments = self.request.session.get('completed_assignments', {})
        completed_assignments[self.object.code] = context['points_earned']
        self.request.session['completed_assignments'] = completed_assignments

        # Clear the user's current assignment.
#        del self.request.session['assignment_code']
        self.request.session.modified = True

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
            'points_earned': assignment.calculate_score(self.request.session['answers']),
            'questions': self.build_question_dicts(
                assignment,
                self.request.session['answers'],
            ),
            'assignee_name': self.request.session['assignee_name'],
            'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
            'BRAND_NAME': settings.BRAND_NAME
        }

        subject = _("{assignment.code} results -- {assignee_name}").format(**context)

        return send_mail.apply_async((
            subject,
            template_instance.render(context),
            settings.DEFAULT_FROM_EMAIL,
            to_address
        ))


