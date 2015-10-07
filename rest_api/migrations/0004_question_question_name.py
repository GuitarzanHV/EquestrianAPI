# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_auto_20151001_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_name',
            field=models.CharField(default='replace', max_length=255),
            preserve_default=False,
        ),
    ]
