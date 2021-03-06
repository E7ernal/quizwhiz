# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 03:36
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify


def forwards(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    School = apps.get_model('quizard', 'School')
    FreeResponseQuestion = apps.get_model('quizard', 'FreeResponseQuestion')
    MultipleChoiceQuestion = apps.get_model('quizard', 'MultipleChoiceQuestion')

    for school in School.objects.using(db_alias).all():
        school.slug = slugify(school.name)
        school.save()

    for question_class in [FreeResponseQuestion, MultipleChoiceQuestion]:
        for question in question_class.objects.using(db_alias).all():
            question.slug = slugify(question.title)
            question.save()


class Migration(migrations.Migration):

    dependencies = [
        ('quizard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='freeresponsequestion',
            name='slug',
            field=models.CharField(max_length=255, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='slug',
            field=models.CharField(max_length=255, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.RunPython(forwards),
        migrations.AlterField(
            model_name='freeresponsequestion',
            name='slug',
            field=models.CharField(max_length=255, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='slug',
            field=models.CharField(max_length=255, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='school',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Slug'),
        ),
    ]
