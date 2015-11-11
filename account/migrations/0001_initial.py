# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.auth.models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], max_length=30, unique=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('level', models.IntegerField(choices=[(1, 'عادی'), (2, 'فعال'), (3, 'مسئول تشکل'), (4, 'استاد پشتیبان'), (5, 'مدیر')], default=1, verbose_name='سطح دسترسی')),
                ('gender', models.IntegerField(choices=[(1, 'برادر'), (2, 'خواهر')], default=1, verbose_name='جنسیت')),
                ('mobile', models.CharField(blank=True, verbose_name='شماره موبایل', null=True, max_length=15, validators=[django.core.validators.RegexValidator(regex='^09\\d{9}$', message='شماره موبایل اشتباه است', code='invalid_mobile')])),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('seen', models.BooleanField(default=False, verbose_name='دیده شده')),
                ('text', models.TextField(verbose_name='متن')),
                ('auto_gen', models.BooleanField(default=True, verbose_name='پیام سیستمی')),
            ],
            options={
                'verbose_name': 'اعلان',
                'verbose_name_plural': 'اعلان ها',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('confirm', models.BooleanField(default=False, verbose_name='تاییدشده')),
            ],
            options={
                'verbose_name': 'تشکل',
                'verbose_name_plural': 'تشکل ها',
            },
        ),
        migrations.CreateModel(
            name='OrganizationMember',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('grade', models.IntegerField(choices=[(1, 'کارشناسی'), (2, 'کارشناسی ارشد'), (3, 'دکتری')], default=1, verbose_name='مقطع تحصیلی')),
                ('enter_year', models.CharField(verbose_name='سال ورود', null=True, max_length=10)),
                ('is_organizer', models.BooleanField(default=False, verbose_name='آیا مسئول تشکل هستید؟')),
                ('expire_date', models.DateField(blank=True, verbose_name='تاریخ اتمام', null=True)),
            ],
            options={
                'verbose_name': 'عضویت در تشکل',
                'verbose_name_plural': 'عضویت ها در تشکل',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='عنوان', max_length=500)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('confirm', models.BooleanField(default=False, verbose_name='تاییدشده')),
            ],
            options={
                'verbose_name': 'حوزه فعالیت',
                'verbose_name_plural': 'حوزه های فعالیت',
            },
        ),
        migrations.CreateModel(
            name='UpgradeMemberRequest',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('last_change', models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)),
                ('first_name', models.CharField(verbose_name='نام', null=True, max_length=300)),
                ('last_name', models.CharField(verbose_name='نام خانوادگی', null=True, max_length=300)),
                ('gender', models.IntegerField(choices=[(1, 'برادر'), (2, 'خواهر')], default=1, verbose_name='جنسیت')),
                ('grade', models.IntegerField(choices=[(1, 'کارشناسی'), (2, 'کارشناسی ارشد'), (3, 'دکتری')], default=1, verbose_name='مقطع تحصیلی')),
                ('enter_year', models.IntegerField(choices=[(1370, 1370), (1371, 1371), (1372, 1372), (1373, 1373), (1374, 1374), (1375, 1375), (1376, 1376), (1377, 1377), (1378, 1378), (1379, 1379), (1380, 1380), (1381, 1381), (1382, 1382), (1383, 1383), (1384, 1384), (1385, 1385), (1386, 1386), (1387, 1387), (1388, 1388), (1389, 1389), (1390, 1390), (1391, 1391), (1392, 1392), (1393, 1393), (1394, 1394)], verbose_name='سال ورود', null=True)),
                ('is_organizer', models.BooleanField(default=False, verbose_name='آیا مسئول تشکل هستید؟')),
                ('mobile', models.CharField(verbose_name='شماره موبایل', null=True, max_length=15)),
                ('state', models.IntegerField(choices=[(1, 'جدید'), (2, 'ویرایش شده'), (3, 'رد شده'), (4, 'تایید شده')], default=1, verbose_name='وضعیت')),
                ('creator', models.ForeignKey(blank=True, related_name='upgradememberrequest_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, related_name='upgradememberrequest_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(to='account.Organization', verbose_name='تشکل', null=True)),
                ('role', models.ForeignKey(to='account.Role', verbose_name='حوزه فعالیت', null=True)),
            ],
            options={
                'verbose_name': 'درخواست ارتقا سطح کاربری',
                'verbose_name_plural': 'درخواست های ارتقا سطح کاربری',
            },
        ),
    ]
