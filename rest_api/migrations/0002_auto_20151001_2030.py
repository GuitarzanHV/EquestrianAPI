# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='rest_api.Question', related_name='answers'),
        ),
        migrations.AlterField(
            model_name='category',
            name='questionnaires',
            field=models.ManyToManyField(to='rest_api.Questionnaire', related_name='categories'),
        ),
        migrations.AlterField(
            model_name='question',
            name='categories',
            field=models.ManyToManyField(to='rest_api.Category', related_name='questions'),
        ),
    ]
