# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

from quizard.models.AbstractBase import AbstractBase


@python_2_unicode_compatible
class MultipleChoiceAnswer(AbstractBase):
    question = models.ForeignKey(
        'quizard.MultipleChoiceQuestion',
        related_name='answers',
        verbose_name=_('Question'),
    )

    value = RichTextField(_('Answer text'))
    is_correct = models.BooleanField(_('Correct'), default=False)

    class Meta:
        verbose_name = _('Multiple choice answer')
        verbose_name_plural = _('Multiple choice answers')

    def __str__(self):
        return "{self.__class__.__name__} #{self.pk}".format(self=self)