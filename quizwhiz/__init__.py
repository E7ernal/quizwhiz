# vim: ts=4:sw=4:expandtabs
from __future__ import absolute_import, unicode_literals

__author__ = 'zach.mott@gmail.com'

import os
from celery import Celery

__all__ = ['celery_app']


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizwhiz.settings')


celery_app = Celery('quizwhiz')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()
