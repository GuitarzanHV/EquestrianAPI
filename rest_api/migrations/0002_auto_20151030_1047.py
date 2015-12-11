# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('display_text', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(null=True, related_name='+', to='rest_api.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='SubcategoryScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('display_text', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='questionnairescore',
            old_name='owner',
            new_name='horse_owner',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.RemoveField(
            model_name='questionscore',
            name='category_score',
        ),
        migrations.RemoveField(
            model_name='questionscore',
            name='score',
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='acceptable_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='display_text',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='name',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categoryscore',
            name='needs_work_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionnairescore',
            name='acceptable_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionnairescore',
            name='display_text',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionnairescore',
            name='horse_name',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionnairescore',
            name='needs_work_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionscore',
            name='display_text',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionscore',
            name='name',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryscore',
            name='questionnaire_score',
            field=models.ForeignKey(null=True, related_name='category_scores', to='rest_api.QuestionnaireScore'),
        ),
        migrations.AlterField(
            model_name='questionnairescore',
            name='questionnaire',
            field=models.ForeignKey(null=True, related_name='+', to='rest_api.Questionnaire'),
        ),
        migrations.AlterField(
            model_name='questionscore',
            name='answer',
            field=models.ForeignKey(null=True, blank=True, related_name='+', to='rest_api.AnswerScore'),
        ),
        migrations.AlterField(
            model_name='questionscore',
            name='question',
            field=models.ForeignKey(null=True, related_name='+', to='rest_api.Question'),
        ),
        migrations.AddField(
            model_name='subcategoryscore',
            name='category_score',
            field=models.ForeignKey(related_name='subcategory_scores', to='rest_api.CategoryScore'),
        ),
        migrations.AddField(
            model_name='subcategoryscore',
            name='subcategory',
            field=models.ForeignKey(null=True, related_name='+', to='rest_api.Subcategory'),
        ),
        migrations.AddField(
            model_name='answerscore',
            name='question_score',
            field=models.ForeignKey(related_name='answer_scores', to='rest_api.QuestionScore'),
        ),
        migrations.AddField(
            model_name='questionscore',
            name='subcategory_score',
            field=models.ForeignKey(default='', related_name='question_scores', to='rest_api.SubcategoryScore'),
            preserve_default=False,
        ),
    ]
