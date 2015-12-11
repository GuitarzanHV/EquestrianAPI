# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def cat_q(apps, schema_editor):
    cs_model = apps.get_model('rest_api', 'CategoryScore')
    qs_model = apps.get_model('rest_api', 'QuestionnaireScore')
    for row in cs_model.objects.all():
        if row.questionnaire_score is None:
            row.category = qs_model.objects.get(pk=1)
            row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_auto_20151113_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnairescore',
            name='owner',
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='riding_style',
            field=models.CharField(default='engl', max_length=4, choices=[('west', 'Western'), ('engl', 'English')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionnairescore',
            name='riding_style',
            field=models.CharField(default='engl', max_length=4),
            preserve_default=False,
        ),
        migrations.RunPython(
	    cat_q,
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
 
