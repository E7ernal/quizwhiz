# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

import random

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

    def get_question(self, question_slug=None, exclude=None):
        if question_slug is None:
            return self.get_random_question(exclude=exclude)
        else:
            return self.get_question_by_slug(question_slug)

    def get_question_by_slug(self, question_slug):
        """
        Get a particular question, as identified by the question_slug.
        Raises ObjectDoesNotExist if the question that slug is not
        related to this Assignment.
        """
        return self.questions.get(proxy__slug=question_slug).question

    def get_random_question(self, exclude=None):
        """
        Gets a random question. exclude is a list of question PKs that
        will be excluded from consideration. Returns None if there are
        no unexcluded questions to make a selection from.
        """
        exclude = exclude or []
        # Regrettably, Django's ORM won't let us do self.questions.exclude
        # with a GenericRelation, so we need to do some list wrangling
        # arithmetic in Python.
        question_pool = filter(
            lambda question: question.pk not in exclude,
            [assignmentquestion.question for assignmentquestion in self.questions.all()]
        )

        try:
            return random.choice(question_pool)
        except IndexError:
            return None
