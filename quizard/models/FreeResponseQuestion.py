# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from quizard.models.BaseQuestion import BaseQuestion


class FreeResponseQuestion(BaseQuestion):
    answer_template = 'quizard/partials/freeresponsequestion/answer.html'

    class Meta:
        verbose_name = _('Free response question')
        verbose_name_plural = _('Free response questions')

    def validate_answer(self, answer):
        case_sensitive = self.answers.filter(value=answer.strip()).exists()
        case_insensitive = self.answers.filter(
            value__iexact=answer.strip(),
            case_sensitive=False
        ).exists()

        return case_sensitive or case_insensitive

