# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('account', '0001_initial'),
        ('experience', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upgradememberrequest',
            name='university',
            field=models.ForeignKey(to='experience.University', verbose_name='دانشگاه', null=True),
        ),
        migrations.AddField(
            model_name='upgradememberrequest',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='role',
            name='creator',
            field=models.ForeignKey(blank=True, related_name='role_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='role',
            name='modifier',
            field=models.ForeignKey(blank=True, related_name='role_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organizationmember',
            name='organization',
            field=models.ForeignKey(to='account.Organization', related_name='organization_members', verbose_name='تشکل'),
        ),
        migrations.AddField(
            model_name='organizationmember',
            name='role',
            field=models.ForeignKey(to='account.Role', related_name='organization_members', verbose_name='حوزه فعالیت'),
        ),
        migrations.AddField(
            model_name='organizationmember',
            name='university',
            field=models.ForeignKey(to='experience.University', related_name='organization_members', verbose_name='دانشگاه'),
        ),
        migrations.AddField(
            model_name='organizationmember',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='organization_members', verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='organization',
            name='creator',
            field=models.ForeignKey(blank=True, related_name='organization_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organization',
            name='modifier',
            field=models.ForeignKey(blank=True, related_name='organization_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='creator',
            field=models.ForeignKey(blank=True, related_name='notification_creators', verbose_name='سازنده', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='modifier',
            field=models.ForeignKey(blank=True, related_name='notification_modifiers', verbose_name='ویرایش کننده', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.ForeignKey(verbose_name='گیرنده', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_set', verbose_name='groups', related_query_name='user', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='user_set', verbose_name='user permissions', related_query_name='user', to='auth.Permission', help_text='Specific permissions for this user.'),
        ),
    ]
