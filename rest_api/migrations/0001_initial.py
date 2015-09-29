# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('answer_text', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('category_name', models.CharField(max_length=255)),
                ('acceptable_score', models.IntegerField(default=0)),
                ('needs_work_score', models.IntegerField(default=0)),
                ('unacceptable_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('question_text', models.CharField(max_length=255)),
                ('question_image', models.CharField(max_length=255)),
                ('categories', models.ManyToManyField(to='rest_api.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('questionnaire_name', models.CharField(max_length=255)),
                ('acceptable_score', models.IntegerField(default=0)),
                ('needs_work_score', models.IntegerField(default=0)),
                ('unacceptable_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='questionnaires',
            field=models.ManyToManyField(to='rest_api.Questionnaire'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='rest_api.Question'),
        ),
    ]
