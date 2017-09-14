# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'
__all__ = ['send_mail']

from django.core.mail import send_mail as django_send_mail


def send_mail(subject, message, from_email, recipient_list, fail_silently=False,
              auth_user=None, auth_password=None, connection=None, html_message=None):
    """
    All email generated by quizard should use this thin wrapper
    around django.core.mail.send_mail. It doesn't do anything
    special right now, but in the future it will log outgoing
    mail in the database.
    """
    return django_send_mail(
        subject, message, from_email, recipient_list,
        fail_silently=fail_silently, auth_user=auth_user,
        auth_password=auth_password, connection=connection,
        html_message=html_message
    )