# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadedComment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('object_pk', models.IntegerField(verbose_name='Object ID')),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('text', models.TextField(null=True)),
                ('tree_path', models.TextField(db_index=True, verbose_name='Tree path', editable=False)),
                ('active', models.BooleanField(default=False, verbose_name='تاییدشده')),
                ('user_name', models.CharField(blank=True, verbose_name='نام', null=True, max_length=255)),
                ('university_name', models.CharField(blank=True, verbose_name='نام دانشگاه', null=True, max_length=255)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='content_type_set_for_threadedcomment', verbose_name='content type')),
                ('last_child', models.ForeignKey(blank=True, to='comment.ThreadedComment', verbose_name='Last child', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, related_name='children', to='comment.ThreadedComment')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='کاربر', null=True)),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
                'ordering': ('tree_path',),
            },
        ),
        migrations.CreateModel(
            name='UserRate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('object_pk', models.IntegerField(verbose_name='Object ID')),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('rate', models.IntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='content_type_set_for_userrate', verbose_name='content type')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='کاربر', null=True)),
            ],
            options={
                'verbose_name': 'امتیاز',
                'verbose_name_plural': 'امتیازها',
            },
        ),
    ]
