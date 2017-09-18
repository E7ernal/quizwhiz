# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from quizard.models.AbstractBase import AbstractBase


@python_2_unicode_compatible
class FreeResponseAnswer(AbstractBase):
    question = models.ForeignKey(
        'quizard.FreeResponseQuestion',
        related_name='answers',
        verbose_name=_('Question'),
    )

    value = models.CharField(_('Answer value'), max_length=255)
    case_sensitive = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Free response answer')
        verbose_name_plural = _('Free response answers')
        unique_together = ('question', 'value')

    def __str__(self):
        return "{self.__class__.__name__} #{self.pk}".format(self=self)
