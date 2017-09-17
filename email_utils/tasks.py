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
        # If this email is being resent, use the existing EmailMessage instance
        email_message = EmailMessage.objects.get(**kw)
    except EmailMessage.DoesNotExist:
        # Otherwise, create a new instance.
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

    # Create a Recipient instance for each address in recipient_list.
    # If a particular address bounces, we blacklist the corresponding
    # recipient record so that we don't try to mail that address in
    # the future.
    for email_address in recipient_list:
        Recipient.objects.get_or_create(address=email_address)

    # Filter out blacklisted emails.
    # Get a list of potential recipients of this email who are blacklisted.
    blacklist = Recipient.objects.filter(
        address__in=recipient_list,
        blacklist=True
    ).values_list('address', flat=True)

    # Remove the blacklisted recipients from recipient_list.
    recipient_list = list(set(recipient_list) - set(blacklist))
    if not recipient_list:
        return None

    email_message.date_sent = timezone.now()

    try:
        num_sent = django_send_mail(
            subject, message, from_email, recipient_list,
            fail_silently=fail_silently, auth_user=auth_user,
            auth_password=auth_password, connection=connection,
            html_message=html_message
        )
    except SMTPRecipientsRefused as smtprr:
        # Delivery was unsuccessful to all of our recipients.
        # Blacklist them to prevent future delivery attempts.
        bounced_addresses = smtprr.recipients.keys()
        error_message = "The following recipients were rejected: {bounces}."
        Recipient.objects.filter(address__in=bounced_addresses).update(blacklist=True)
        email_message.delivery_successful = False
        email_message.error_message = error_message.format(bounces=', '.join(bounced_addresses))
    except SMTPException as smtpe:
        email_message.delivery_successful = False
        email_message.error_message = smtpe.smtp_error
    else:
        email_message.delivery_successful = True
    finally:
        email_message.save()

    return num_sent
