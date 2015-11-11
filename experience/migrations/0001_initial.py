# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('confirm', models.BooleanField(default=False, verbose_name='تاییدشده')),
                ('publish_type', models.IntegerField(choices=[(1, 'عمومی'), (2, 'خاص اعضای فعال'), (3, 'خاص مسئول تشکل ها')], default=1, verbose_name='نوع انتشار')),
                ('visitor_count', models.IntegerField(default=0, verbose_name='تعداد بازدید')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('date', models.DateField(verbose_name='تاریخ تجربه')),
                ('image', models.ImageField(verbose_name='تصویر', null=True, upload_to='experience_image/')),
                ('image_cropping', image_cropping.fields.ImageRatioField('image', '128x292', hide_image_field=False, allow_fullsize=False, adapt_rotation=False, size_warning=False, free_crop=False, verbose_name='محدوده کراپ برای لیست', help_text='')),
                ('service', models.IntegerField(choices=[(1, 'شهدا و دفاع\u200cمقدس'), (2, 'جهان اسلام و مستضعفین'), (3, 'اردویی'), (4, 'رشد و کادرسازی'), (5, 'نقش آفرینی علمی'), (6, 'مسائل تشکیلاتی'), (7, 'جذب و ورودی جدید'), (8, 'نقش آفرینی حاکمیتی'), (9, 'رسانه و هنر'), (10, 'آزادفکری'), (11, 'جهادی'), (12, 'مسجد و هیئت')], verbose_name='سرویس', null=True)),
                ('comment_count', models.IntegerField(default=0, verbose_name='تعداد کامنت ها')),
                ('rate', models.FloatField(default=0, verbose_name='امتیاز')),
                ('creator', models.ForeignKey(blank=True, related_name='experience_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('gallery', models.ForeignKey(to='utils.Gallery', verbose_name='گالری', null=True)),
                ('modifier', models.ForeignKey(blank=True, related_name='experience_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(to='account.Organization', verbose_name='تشکل', null=True)),
            ],
            options={
                'verbose_name': 'تجربه',
                'verbose_name_plural': 'تجربه ها',
            },
        ),
        migrations.CreateModel(
            name='ExperienceAttachment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('attach', models.FileField(verbose_name='فایل', upload_to='experience_attachments/')),
                ('experience', models.ForeignKey(to='experience.Experience', related_name='attachments')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('creator', models.ForeignKey(blank=True, related_name='place_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='place_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'محل',
                'verbose_name_plural': 'محل ها',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('confirm', models.BooleanField(default=False, verbose_name='تاییدشده')),
                ('creator', models.ForeignKey(blank=True, related_name='tag_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='tag_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ ها',
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('confirm', models.BooleanField(default=False, verbose_name='تاییدشده')),
                ('uni_type', models.IntegerField(choices=[(1, 'دولتی'), (2, 'آزاد'), (3, 'پیام نور'), (4, 'غیر انتفاعی'), (5, 'علوم پزشکی'), (6, 'فرهنگیان'), (7, 'علمی-کاربردی')], verbose_name='نوع', null=True)),
                ('image', models.ImageField(verbose_name='تصویر', null=True, upload_to='university_image/')),
                ('creator', models.ForeignKey(blank=True, related_name='university_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='university_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(to='experience.Place', verbose_name='استان', null=True)),
            ],
            options={
                'verbose_name': 'دانشگاه',
                'verbose_name_plural': 'دانشگاه ها',
            },
        ),
        migrations.AddField(
            model_name='experience',
            name='tags',
            field=models.ManyToManyField(to='experience.Tag', related_name='experiences', verbose_name='تگ ها'),
        ),
        migrations.AddField(
            model_name='experience',
            name='university',
            field=models.ForeignKey(to='experience.University', verbose_name='دانشگاه', null=True),
        ),
    ]
