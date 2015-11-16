# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0003_auto_20151104_0641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='image_cropping',
        ),
        migrations.AlterField(
            model_name='experience',
            name='date',
            field=models.DateField(verbose_name='تاریخ تجربه', blank=True, null=True),
        ),
    ]
