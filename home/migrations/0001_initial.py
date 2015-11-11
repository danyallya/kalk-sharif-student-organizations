# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('document', '0001_initial'),
        ('experience', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeExp',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('creator', models.ForeignKey(blank=True, related_name='homeexp_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('experience', models.OneToOneField(to='experience.Experience', verbose_name='تجربه')),
                ('modifier', models.ForeignKey(blank=True, related_name='homeexp_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'تجربیات صفحه اول',
                'verbose_name_plural': 'تجربیات صفحه اول',
            },
        ),
        migrations.CreateModel(
            name='HomePackage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('creator', models.ForeignKey(blank=True, related_name='homepackage_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='homepackage_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
                ('package', models.OneToOneField(to='document.BackupPackage', verbose_name='بسته پشتیبان')),
            ],
            options={
                'verbose_name': 'تجربیات صفحه اول',
                'verbose_name_plural': 'تجربیات صفحه اول',
            },
        ),
        migrations.CreateModel(
            name='SliderItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('image', image_cropping.fields.ImageCropField(verbose_name='تصویر', null=True, upload_to='slider_image/')),
                ('image_cropping', image_cropping.fields.ImageRatioField('image', '1020x386', hide_image_field=False, allow_fullsize=False, adapt_rotation=False, size_warning=False, free_crop=False, verbose_name='محدوده کراپ', help_text='')),
                ('text', models.TextField(verbose_name='متن', null=True)),
                ('link', models.URLField(verbose_name='لینک', null=True)),
                ('active', models.BooleanField(default=True, verbose_name='فعال')),
                ('creator', models.ForeignKey(blank=True, related_name='slideritem_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='slideritem_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'اسلاید',
                'verbose_name_plural': 'اسلاید ها',
            },
        ),
    ]
