# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rest_api', '0002_auto_20151030_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
            model_name='questionnairescore',
            name='location',
            field=models.CharField(default='testing', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionnairescore',
            name='mobile',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='questionnairescore',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, related_name='questionnaire_scores', to=settings.AUTH_USER_MODEL),
        ),
    ]
