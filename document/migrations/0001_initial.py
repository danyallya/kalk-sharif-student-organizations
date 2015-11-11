# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.fields.file_fields
import image_cropping.fields
import colorful.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experience', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackupPackage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('confirm', models.BooleanField(default=False, verbose_name='تاییدشده')),
                ('publish_type', models.IntegerField(choices=[(1, 'عمومی'), (2, 'خاص اعضای فعال'), (3, 'خاص مسئول تشکل ها')], default=1, verbose_name='نوع انتشار')),
                ('visitor_count', models.IntegerField(default=0, verbose_name='تعداد بازدید')),
                ('pdf_file', utils.fields.file_fields.ContentTypeRestrictedFileField(verbose_name='فایل', null=True, upload_to='backup_package/')),
                ('image', models.ImageField(blank=True, verbose_name='تصویر', null=True, upload_to='backup_package_image/')),
                ('receive_count', models.IntegerField(default=0, verbose_name='تعداد دانلود')),
                ('rate', models.FloatField(default=0, verbose_name='امتیاز')),
            ],
            options={
                'verbose_name': 'بسته پشتیبان',
                'verbose_name_plural': 'بسته های پشتیبان',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('publish_type', models.IntegerField(choices=[(1, 'عمومی'), (2, 'خاص اعضای فعال'), (3, 'خاص مسئول تشکل ها')], default=1, verbose_name='نوع انتشار')),
                ('visitor_count', models.IntegerField(default=0, verbose_name='تعداد بازدید')),
                ('image', image_cropping.fields.ImageCropField(verbose_name='تصویر', null=True, upload_to='document_image/')),
                ('file', models.FileField(blank=True, verbose_name='نقشه عملیاتی', null=True, upload_to='document_file/')),
                ('intro', models.TextField(blank=True, verbose_name='مقدمه', null=True)),
                ('list_text', models.TextField(blank=True, verbose_name='متن صفحه اسناد', null=True)),
                ('service', models.IntegerField(choices=[(1, 'شهدا و دفاع\u200cمقدس'), (2, 'جهان اسلام و مستضعفین'), (3, 'اردویی'), (4, 'رشد و کادرسازی'), (5, 'نقش آفرینی علمی'), (6, 'مسائل تشکیلاتی'), (7, 'جذب و ورودی جدید'), (8, 'نقش آفرینی حاکمیتی'), (9, 'رسانه و هنر'), (10, 'آزادفکری'), (11, 'جهادی'), (12, 'مسجد و هیئت')], default=1, verbose_name='سرویس', null=True)),
                ('animate_type', models.IntegerField(choices=[(1, 'از پایین'), (2, 'از راست'), (3, 'از چپ')], default=1, verbose_name='نوع انیمیشن', null=True)),
                ('order', models.IntegerField(default=1, verbose_name='اولویت در لیست', null=True)),
                ('image_cropping', image_cropping.fields.ImageRatioField('image', '240x240', hide_image_field=False, allow_fullsize=False, adapt_rotation=False, size_warning=False, free_crop=False, verbose_name='محدوده کراپ برای لیست', help_text='')),
                ('comment_count', models.IntegerField(default=0, verbose_name='تعداد کامنت ها')),
                ('rate', models.FloatField(default=0, verbose_name='امتیاز')),
                ('color', colorful.fields.RGBColorField(default='#0b3f57', verbose_name='رنگ')),
                ('creator', models.ForeignKey(blank=True, related_name='document_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='document_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='documents', verbose_name='تگ ها', to='experience.Tag')),
            ],
            options={
                'verbose_name': 'سند',
                'verbose_name_plural': 'سندها',
            },
        ),
        migrations.CreateModel(
            name='DocumentLevel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('text', models.TextField(blank=True, verbose_name='متن', null=True)),
                ('color', colorful.fields.RGBColorField(default='#000000', verbose_name='رنگ')),
                ('depth', models.IntegerField(default=1, verbose_name='سطح')),
                ('comment_count', models.IntegerField(default=0, verbose_name='تعداد دیدگاه ها')),
                ('creator', models.ForeignKey(blank=True, related_name='documentlevel_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(to='document.Document', related_name='levels', verbose_name='سند')),
                ('modifier', models.ForeignKey(blank=True, related_name='documentlevel_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, default=None, verbose_name='دربرگیرنده', null=True, related_name='children', to='document.DocumentLevel')),
                ('references', models.ManyToManyField(blank=True, related_name='document_levels', verbose_name='تجربیات ارجاع شده', to='experience.Experience')),
            ],
            options={
                'verbose_name': 'طبقه سند',
                'verbose_name_plural': 'طبقه های سند',
            },
        ),
        migrations.CreateModel(
            name='PackageSubCat',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('cat', models.IntegerField(choices=[(1, 'چندرسانه ای'), (2, 'اساتید و اشخاص'), (3, 'مکان یابی'), (4, 'کتابخانه'), (5, 'اردویی'), (6, 'آیین نامه')], default=1, verbose_name='دسته بندی')),
                ('icon', models.ImageField(verbose_name='آیکن', upload_to='package_cat_icons/')),
                ('creator', models.ForeignKey(blank=True, related_name='packagesubcat_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='packagesubcat_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'دسته بسته پشتیبان',
                'verbose_name_plural': 'دسته های بسته پشتیبان',
            },
        ),
        migrations.CreateModel(
            name='SpecificDocument',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('creator', models.ForeignKey(blank=True, related_name='specificdocument_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('doc', models.OneToOneField(to='document.Document', related_name='spec', verbose_name='سند')),
                ('modifier', models.ForeignKey(blank=True, related_name='specificdocument_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'سند برگزیده',
                'verbose_name_plural': 'اسناد برگزیده',
            },
        ),
        migrations.AddField(
            model_name='backuppackage',
            name='cat',
            field=models.ForeignKey(to='document.PackageSubCat', default=None, verbose_name='دسته بندی', null=True),
        ),
        migrations.AddField(
            model_name='backuppackage',
            name='creator',
            field=models.ForeignKey(blank=True, related_name='backuppackage_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='backuppackage',
            name='document',
            field=models.ForeignKey(to='document.Document', related_name='packages', verbose_name='سند', null=True),
        ),
        migrations.AddField(
            model_name='backuppackage',
            name='modifier',
            field=models.ForeignKey(blank=True, related_name='backuppackage_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='backuppackage',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='backups', verbose_name='تگ ها', to='experience.Tag'),
        ),
        migrations.AddField(
            model_name='backuppackage',
            name='university',
            field=models.ForeignKey(to='experience.University', default=1, verbose_name='دانشگاه', null=True),
        ),
    ]
