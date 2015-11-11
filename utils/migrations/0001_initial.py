# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='HelpCase',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('code', models.CharField(choices=[('logo', 'کل سایت | لوگو کالک'), ('header-map-first', 'کل سایت | نقشه سایت 1'), ('header-map-second', 'کل سایت | نقشه سایت 2'), ('header-map-third', 'کل سایت | نقشه سایت 3'), ('send-image-header', 'تجربه | ارسال تصاویر شما'), ('experience-share-header', 'تجربه | معرفی به دیگران'), ('experience-complement-header', 'تجربه | تکمیل این تجربه'), ('experience-comments-panel', 'تجربه | پرسش و پاسخ'), ('experience-title', 'تجربه | عنوان تجربه'), ('experience-uni', 'تجربه | دانشگاه تجربه'), ('experience-author', 'تجربه | نویسنده تجربه'), ('experience-date', 'تجربه | تاریخ تجربه'), ('experience-content', 'تجربه | متن تجربه'), ('experience-right-title', 'تجربه | عنوان سمت راست تجربه'), ('experience-image', 'تجربه | عکس تجربه'), ('text-attachment', 'تجربه | متن ضمیمه'), ('video-attachment', 'تجربه | ویدیو ضمیمه'), ('link-attachment', 'تجربه | لینک ضمیمه'), ('image-attachment', 'تجربه | تصویر ضمیمه'), ('experience-related-ex', 'تجربه | تجربیات مرتبط'), ('experience-content', 'تجربه | متن تجربه'), ('experience-extra-images', 'تجربه | عکس های تجربه'), ('send-image-div', 'تجربه | بارگزاری تصویرهای شما'), ('show-all-images', 'تجربه | مشاهده همه تصاویر'), ('experience-rating', 'سند | امتیازدهی'), ('doc-action-map', 'سند | دریافت نقشه عملیاتی'), ('doc-your-experience', 'سند | تجربه شما'), ('doc-help', 'سند | راهنما'), ('doc-page-tree', 'سند | درختی سند'), ('doc-content', 'سند | متن سند'), ('doc-reference-tab', 'سند | تجربیات ارجاع شده'), ('doc-comments-tab', 'سند | دیدگاه ها و نظرات'), ('comments_link', 'سند | دیدگاه'), ('refs_link', 'سند | ارجاع'), ('document-rating', 'سند | امتیازدهی')], verbose_name='عنصر', max_length=100, unique=True)),
                ('text', models.CharField(default='', verbose_name='متن', max_length=500)),
                ('creator', models.ForeignKey(blank=True, related_name='helpcase_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='helpcase_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'راهنما',
                'verbose_name_plural': 'راهنما ها',
            },
        ),
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('image', models.ImageField(verbose_name='تصویر', upload_to='images/')),
                ('confirm', models.BooleanField(default=True, verbose_name='تاییدشده')),
                ('gallery', models.ForeignKey(to='utils.Gallery', related_name='images', verbose_name='گالری')),
            ],
        ),
    ]
