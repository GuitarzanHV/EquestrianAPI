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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('display_text', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
                ('acceptable_score', models.IntegerField(default=0)),
                ('needs_work_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('category', models.ForeignKey(to='rest_api.Category', related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
                ('image', models.FilePathField(path='/var/www/images', blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
                ('acceptable_score', models.IntegerField(default=0)),
                ('needs_work_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionnaireScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('owner', models.CharField(max_length=60)),
                ('date_started', models.DateField(auto_now_add=True)),
                ('date_last_edited', models.DateField(auto_now=True)),
                ('questionnaire', models.ForeignKey(to='rest_api.Questionnaire', related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('score', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(to='rest_api.Answer', blank=True, related_name='+', null=True)),
                ('category_score', models.ForeignKey(to='rest_api.CategoryScore', related_name='question_scores')),
                ('question', models.ForeignKey(to='rest_api.Question', related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
                ('categories', models.ManyToManyField(to='rest_api.Category', related_name='subcategories')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='subcategory',
            field=models.ForeignKey(to='rest_api.Subcategory', related_name='questions'),
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='questionnaire_score',
            field=models.ForeignKey(to='rest_api.QuestionnaireScore', related_name='category_scores'),
        ),
        migrations.AddField(
            model_name='category',
            name='questionnaires',
            field=models.ManyToManyField(to='rest_api.Questionnaire', related_name='categories'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='rest_api.Question', related_name='answers'),
        ),
    ]
