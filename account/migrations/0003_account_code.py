# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151031_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='code',
            field=models.CharField(blank=True, null=True, max_length=200, verbose_name='کد فراموشی رمز عبور'),
        ),
    ]
