# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

from quizard.models import AbstractBase


@python_2_unicode_compatible
class Assignment(AbstractBase):
    school = models.ForeignKey('quizard.School', verbose_name=_('School'), blank=True, null=True)

    name = models.CharField(_('Name'), max_length=255)
    code = models.CharField(_('Code'), max_length=16, unique=True)
    summary = RichTextField(_('Summary'), blank=True)
    description = RichTextField(_('Description'), blank=True)
    is_private = models.BooleanField(_('Private'), default=False)

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')

    def __str__(self):
        return self.name

    @cached_property
    def num_questions(self):
        return self.questions.count()
    num_questions.short_description = _('Number of questions')