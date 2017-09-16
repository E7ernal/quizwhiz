# vim: ts=4:sw=4:expandtabs
from __future__ import absolute_import, unicode_literals

__author__ = 'zach.mott@gmail.com'

from django.utils import timezone

from celery import shared_task

__all__ = ['send_mail']


@shared_task
def send_mail(subject, message, from_email, recipients, fail_silently=False,
              auth_user=None, auth_password=None, connection=None, html_message=''):
    """
    Utility task for sending email.
    - It's a celery task, so it can be run asynchronously.
    - It logs all outgoing mail, along with delivery status, to the database.
    """
    from smtplib import SMTPException, SMTPRecipientsRefused
    from django.core.mail import send_mail as django_send_mail
    from email_utils.models import EmailMessage, Recipient

    num_sent = 0

    kw = {
        'to': recipients,
        'from_address': from_email,
        'subject': subject,
        'body': message,
        'html_body': html_message
    }

    try:
        email_message = EmailMessage.objects.get(**kw)
    except EmailMessage.DoesNotExist:
        email_message = EmailMessage(**kw)

    # Make a bona fide attempt to figure out who this email
    # is supposed to go to.
    if isinstance(recipients, list) or isinstance(recipients, tuple):
        recipient_list = recipients
    else:
        try:
            recipient_list = recipients.split(',')
        except AttributeError:
            return None

    email_message.date_sent = timezone.now()

    try:
        num_sent = django_send_mail(
            subject, message, from_email, recipient_list,
            fail_silently=fail_silently, auth_user=auth_user,
            auth_password=auth_password, connection=connection,
            html_message=html_message
        )
#    except SMTPRecipientsRefused as smtprr:
#        pass
    except SMTPException as smtpe:
        email_message.delivery_successful = False
        email_message.error_message = smtpe.smtp_error
    else:
        email_message.delivery_successful = True
    finally:
        email_message.save()

    return num_sent
