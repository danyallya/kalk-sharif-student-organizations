# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0002_auto_20151103_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='creator_old',
            field=models.CharField(blank=True, verbose_name='نویسنده', null=True, max_length=255),
        ),
        migrations.AddField(
            model_name='experience',
            name='uni_temp',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
    ]
