# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

import random

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

from quizard.models import AbstractBase


class AssignmentManager(models.Manager):
    def get_queryset(self):
        return super(AssignmentManager, self).get_queryset().prefetch_related('questions')


@python_2_unicode_compatible
class Assignment(AbstractBase):
    class OutOfQuestions(ValueError):
        pass

    school = models.ForeignKey('quizard.School', verbose_name=_('School'), blank=True, null=True)

    name = models.CharField(_('Name'), max_length=255)
    code = models.CharField(_('Code'), max_length=16, unique=True)
    summary = RichTextField(_('Summary'), blank=True)
    description = RichTextField(_('Description'), blank=True)
    is_private = models.BooleanField(_('Private'), default=False)

    objects = AssignmentManager()

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')

    def __str__(self):
        return self.name

    @cached_property
    def num_questions(self):
        return self.questions.count()
    num_questions.short_description = _('Number of questions')

    @cached_property
    def total_points(self):
        # It would be nice to do this in the database, but the generic
        # relation between AssignmentQuestion and BaseQuestion makes that
        # very difficult to do.
        return reduce(lambda x, y: x + y, [q.point_value for q in self.questions.all()])

    def calculate_score(self, answers):
        """
        Calculate the total number of points earned by a particular set
        of answers. 'answers' is a dict that maps {question.pk: answer_text}.
        """
        score = 0

        for question_pk, answer in answers.iteritems():
            try:
                question = self.get_question_by_pk(question_pk)
                if question.validate_answer(answer):
                    score += question.point_value
            except models.ObjectDoesNotExist:
                print "Couldn't find question", question_pk

        return score

    def get_question_by_pk(self, question_pk):
        """
        Get the question provided by the given question_pk. Raises
        ObjectDoesNotExist if no such question is attached to this
        Assignment.
        """
        for question in self.questions.all():
            if int(question.pk) == int(question_pk):
                return question

        raise models.ObjectDoesNotExist()

    def get_question_by_slug(self, question_slug):
        """
        Get a particular question, as identified by the question_slug.
        Raises ObjectDoesNotExist if the slugs' question  is not
        related to this Assignment. Can't do this in the database 'cause
        generic relations.
        """
        for question in self.questions.all():
            if question.slug == question_slug:
                return question

        raise models.ObjectDoesNotExist()

    def get_random_question(self, exclude=None):
        """
        Gets a random question. 'exclude' is a list of question PKs that
        will be excluded from consideration. Returns None if there are
        no unexcluded questions to make a selection from.
        """
        exclude = exclude or []
        # Regrettably, Django's ORM won't let us do self.questions.exclude
        # with a GenericRelation, so we need to do some list wrangling
        # arithmetic in Python.
        question_pool = filter(
            lambda question: question.pk not in exclude,
            [assignmentquestion for assignmentquestion in self.questions.all()]
        )

        try:
            return random.choice(question_pool)
        except IndexError:
            raise self.OutOfQuestions()
