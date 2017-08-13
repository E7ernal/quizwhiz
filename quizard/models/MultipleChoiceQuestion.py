# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from quizard.models.BaseQuestion import BaseQuestion


class MultipleChoiceQuestion(BaseQuestion):
    answer_template = 'quizard/partials/multiplechoicequestion/answers.html'

    class Meta:
        verbose_name = _('Multiple choice question')
        verbose_name_plural = _('Multiple choice questions')

    def validate_answer(self, answer):
        return self.answers.filter(value=answer.strip(), is_correct=True).exists()
