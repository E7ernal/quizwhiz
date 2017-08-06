# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'


from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

from quizard.models.AbstractBase import AbstractBase


@python_2_unicode_compatible
class School(AbstractBase):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    pretty_name = RichTextField(_('Pretty name'), blank=True)

    class Meta:
        verbose_name = _('School')
        verbose_name_plural = _('Schools')
        ordering = ['name']

    def __str__(self):
        return self.name
