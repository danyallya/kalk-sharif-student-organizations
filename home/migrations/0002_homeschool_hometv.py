# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0004_auto_20151116_2109'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeSchool',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('visitor_count', models.IntegerField(default=0, verbose_name='تعداد بازدید')),
                ('image', models.ImageField(null=True, verbose_name='تصویر', upload_to='experience_image/')),
                ('service', models.IntegerField(choices=[(1, 'شهدا و دفاع\u200cمقدس'), (2, 'جهان اسلام و مستضعفین'), (3, 'اردویی'), (4, 'رشد و کادرسازی'), (5, 'نقش آفرینی علمی'), (6, 'مسائل تشکیلاتی'), (7, 'جذب و ورودی جدید'), (8, 'نقش آفرینی حاکمیتی'), (9, 'رسانه و هنر'), (10, 'آزادفکری'), (11, 'جهادی'), (12, 'مسجد و هیئت')], verbose_name='سرویس', null=True)),
                ('creator', models.ForeignKey(verbose_name='سازنده', related_name='homeschool_creators', blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(verbose_name='ویرایش کننده', related_name='homeschool_modifiers', blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'مدرسته کالک صفحه اول',
                'verbose_name': 'مدرسته کالک صفحه اول',
            },
        ),
        migrations.CreateModel(
            name='HomeTV',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('text', models.TextField(default='', verbose_name='متن', blank=True)),
                ('date', models.DateField(null=True, verbose_name='تاریخ', blank=True)),
                ('image', models.ImageField(null=True, verbose_name='تصویر', upload_to='experience_image/')),
                ('page_place', models.IntegerField(choices=[(1, 'ویدیو اصلی'), (2, 'ویدیو سمت چپ'), (3, 'اسلایدر ویدیو')], verbose_name='مکان در صفحه', blank=True, null=True)),
                ('creator', models.ForeignKey(verbose_name='سازنده', related_name='hometv_creators', blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(verbose_name='ویرایش کننده', related_name='hometv_modifiers', blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('university', models.ForeignKey(verbose_name='دانشگاه', blank=True, null=True, to='experience.University')),
            ],
            options={
                'verbose_name_plural': 'کالک TV صفحه اول',
                'verbose_name': 'کالک TV صفحه اول',
            },
        ),
    ]
