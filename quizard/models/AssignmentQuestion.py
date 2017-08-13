# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey

from gfklookupwidget.fields import GfkLookupField

from quizard.models.AbstractBase import AbstractBase


class AssignmentQuestionManager(models.Manager):
    def get_queryset(self):
        return super(AssignmentQuestionManager, self).get_queryset().prefetch_related('question')


@python_2_unicode_compatible
class AssignmentQuestion(AbstractBase):
    # When asked for one of these properties, AssignmentQuestion will
    # proxy the attribute request to its underlying question.
    proxied_properties = [
        'title', 'slug', 'point_value', 'explanation',
        'html', 'answer_template', 'answers', 'validate_answer',
    ]

    assignment = models.ForeignKey(
        'quizard.Assignment',
        verbose_name=_('Assignment'),
        related_name='questions'
    )

    index = models.PositiveIntegerField(_('Index'))

    question_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_('Question type'),
        limit_choices_to={
            'app_label': 'quizard',
            'model__in': ['multiplechoicequestion', 'freeresponsequestion'],
        },
    )
    question_id = GfkLookupField('question_type', _('Question ID'))
    question = GenericForeignKey('question_type', 'question_id')

    objects = AssignmentQuestionManager()

    class Meta:
        verbose_name = _('Assignment question')
        verbose_name_plural = _('Assignment questions')
        ordering = ['index']
        unique_together = ('question_type', 'question_id', 'assignment')

    def __str__(self):
        return "{self.assignment}: {self.question_type.model} #{self.index}".format(self=self)

    def __getattribute__(self, item):
        supercall = super(AssignmentQuestion, self).__getattribute__
        if item in supercall('proxied_properties'):
            return getattr(self.question, item)
        return supercall(item)
