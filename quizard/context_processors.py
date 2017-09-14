# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.conf import settings


def quizard_settings(request):
    return {
        'BRAND_NAME': settings.BRAND_NAME,
        'DOMAIN_NAME': settings.DOMAIN_NAME,
        'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
    }