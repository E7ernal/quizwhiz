# vim: ts=4:sw=4:expandtabs
from __future__ import absolute_import, unicode_literals

__author__ = 'zach.mott@gmail.com'

import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizwhiz.settings')


app = Celery('quizwhiz')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def add(*pos):
    return sum(pos)
