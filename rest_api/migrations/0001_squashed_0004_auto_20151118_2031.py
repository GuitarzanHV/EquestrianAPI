# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# rest_api.migrations.0004_auto_20151118_2031

class Migration(migrations.Migration):

    replaces = [('rest_api', '0001_initial'), ('rest_api', '0002_auto_20151030_1047'), ('rest_api', '0003_auto_20151113_1312'), ('rest_api', '0004_auto_20151118_2031')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('display_text', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
                ('acceptable_score', models.IntegerField(default=0)),
                ('needs_work_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryScore',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('category', models.ForeignKey(to='rest_api.Category', related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
                ('image', models.FilePathField(default='', path='/var/www/images', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
                ('acceptable_score', models.IntegerField(default=0)),
                ('needs_work_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionnaireScore',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('horse_owner', models.CharField(max_length=60)),
                ('date_started', models.DateField(auto_now_add=True)),
                ('date_last_edited', models.DateField(auto_now=True)),
                ('questionnaire', models.ForeignKey(to='rest_api.Questionnaire', null=True, related_name='+')),
                ('acceptable_score', models.IntegerField(default=0)),
                ('display_text', models.CharField(default='', max_length=100)),
                ('horse_name', models.CharField(default='', max_length=20)),
                ('needs_work_score', models.IntegerField(default=0)),
                ('location', models.CharField(default='testing', max_length=100)),
                ('mobile', models.BooleanField(default=True)),
                ('riding_style', models.CharField(default='engl', max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionScore',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('answer', models.ForeignKey(blank=True, to='rest_api.AnswerScore', null=True, related_name='+')),
                ('question', models.ForeignKey(to='rest_api.Question', null=True, related_name='+')),
                ('display_text', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
            field=models.ForeignKey(to='rest_api.QuestionnaireScore', null=True, related_name='category_scores'),
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
        migrations.CreateModel(
            name='AnswerScore',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('display_text', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(to='rest_api.Answer', null=True, related_name='+')),
                ('question_score', models.ForeignKey(to='rest_api.QuestionScore', related_name='answer_scores')),
            ],
        ),
        migrations.CreateModel(
            name='SubcategoryScore',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='acceptable_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='display_text',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='needs_work_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subcategoryscore',
            name='category_score',
            field=models.ForeignKey(to='rest_api.CategoryScore', related_name='subcategory_scores'),
        ),
        migrations.AddField(
            model_name='subcategoryscore',
            name='subcategory',
            field=models.ForeignKey(to='rest_api.Subcategory', null=True, related_name='+'),
        ),
        migrations.AddField(
            model_name='questionscore',
            name='subcategory_score',
            field=models.ForeignKey(default='', to='rest_api.SubcategoryScore', related_name='question_scores'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('display_word_text', models.CharField(max_length=20)),
                ('display_definition_text', models.CharField(max_length=600)),
            ],
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='mobile',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='riding_style',
            field=models.CharField(default='engl', max_length=4, choices=[('west', 'Western'), ('engl', 'English')]),
            preserve_default=False,
        ),
        migrations.RunPython(
            code=rest_api.migrations.0004_auto_20151118_2031.cat_q,
        ),
        migrations.AlterField(
            model_name='categoryscore',
            name='category',
            field=models.ForeignKey(to='rest_api.Category', null=True, related_name='+'),
        ),
        migrations.AlterField(
            model_name='categoryscore',
            name='questionnaire_score',
            field=models.ForeignKey(to='rest_api.QuestionnaireScore', related_name='category_scores'),
        ),
    ]
