# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig, apps
from django.db.models.signals import post_save


class QuizardConfig(AppConfig):
    name = 'quizard'

    def ready(self):
        post_save.connect(create_user_folder, apps.get_model('auth', 'User'))


def create_user_folder(sender, instance, **kwargs):
    from filer.models.foldermodels import Folder, FolderPermission

    if instance.is_staff:
        folder, _ = Folder.objects.get_or_create(
            name=instance.username,
            owner=instance
        )

        FolderPermission.objects.get_or_create(
            folder=folder,
            user=instance,
            defaults={
                'type': FolderPermission.CHILDREN,
                'can_edit': True,
                'can_read': True,
                'can_add_children': True
            }
        )
