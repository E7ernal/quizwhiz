# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

from quizard.models.AbstractBase import AbstractBase


@python_2_unicode_compatible
class BaseQuestion(AbstractBase):
    """
    Declares fields common to all question types.
    """
    created_by = models.ForeignKey('auth.User', verbose_name=_('Created by'))

    point_value = models.PositiveIntegerField(_('Point value'))
    explanation = RichTextField(_('Explanation'))
    html = RichTextField(_('Question text'))

    class Meta:
        abstract = True

    def __str__(self):
        return "{self.__class__.__name__} #{self.pk} ({self.point_value} point(s))".format(self=self)
