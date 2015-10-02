# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0002_auto_20151001_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='acceptable_score',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='acceptable_score',
        ),
    ]
