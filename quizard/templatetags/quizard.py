# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

import random

from django.template import Library, TemplateDoesNotExist
from django.template.loader import get_template
from django.core.exceptions import ImproperlyConfigured

register = Library()


@register.simple_tag(takes_context=True)
def render_answers(context, question):
    try:
        template = get_template(question.answer_template)
    except TemplateDoesNotExist:
        raise ImproperlyConfigured('Subclasses of BaseQuestion must define '
                                   'a non-None answer_template property.')

    # random.shuffle modifies a list in-place.
    answers = list(question.answers.all())
    random.shuffle(answers)

    return template.render({
        'question': question,
        'answers': answers,
        'submitted_answer': context['submitted_answer']
    }, context.request)
