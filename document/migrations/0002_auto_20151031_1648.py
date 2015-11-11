# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backuppackage',
            name='university',
        ),
        migrations.AlterField(
            model_name='backuppackage',
            name='document',
            field=models.ForeignKey(blank=True, verbose_name='سند', null=True, to='document.Document', related_name='packages'),
        ),
    ]
