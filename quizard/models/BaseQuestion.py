# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor.fields import RichTextField

from quizard.models.AbstractBase import AbstractBase


class BaseQuestionManager(models.Manager):
    def get_queryset(self):
        return super(BaseQuestionManager, self).get_queryset().prefetch_related('answers')


@python_2_unicode_compatible
class BaseQuestion(AbstractBase):
    """
    Declares fields common to all question types.
    """
    answer_template = None

    created_by = models.ForeignKey('auth.User', verbose_name=_('Created by'))

    title = models.CharField(_('Title'), max_length=255)
    slug = models.CharField(_('Slug'), max_length=255, unique=True)
    point_value = models.PositiveIntegerField(_('Point value'))
    explanation = RichTextField(_('Explanation'))
    html = RichTextField(_('Question text'))

    objects = BaseQuestionManager()

    class Meta:
        abstract = True
        unique_together = ('title', 'created_by')

    def __str__(self):
        return self.title

    def validate_answer(self, answer):
        raise NotImplementedError('Inheriting class must implement this method!')
