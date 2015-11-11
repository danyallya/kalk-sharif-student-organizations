# -*- coding:utf-8 -*-
import datetime
from django.utils import formats
from django.utils.html import avoid_wrapping
from account.models import Notification
from account.permissions import PermissionController
from experience.models import Place
from utils.calverter import gregorian_to_jalali, gregorian_to_jalaliyear, gregorian_to_jalaliyearmonth, \
    gregorian_to_jalaliyearmonthday

__author__ = 'M.Y'
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_dict(input_dict, key):
    return input_dict.get(key)


@register.simple_tag
def welcome_st(user):
    overall_name = u"%s %s" % (user.first_name, user.last_name) if (
        user.first_name and user.last_name) else u"%s" % user.username
    return u"%s خوش آمدید." % overall_name


@register.filter
def is_false(value):
    return value is False or value == 'False'


@register.simple_tag(takes_context=True)
def render_url_li(context, url, persian_name):
    # url = reverse(name)
    html_class = 'active' if context.get('request').path == url else ''
    res = u"""
    <li>
        <a href="%s%s" class="%s">
            %s
        </a>
    </li>
    """ % (settings.SITE_URL, url, html_class, persian_name)
    return res


@register.simple_tag(takes_context=True)
def get_current_menu_name(context, menus):
    for menu in menus:
        if context.get('request').path == menu.url:
            return menu.show_name
    return u"صفحه اصلی"


@register.filter
def is_true(value):
    return value is True


@register.filter
def get_field(instance, name):
    return getattr(instance, name).all()


@register.filter
def pdate_if_date(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalali(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value


@register.filter
def pdate_year(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalaliyear(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value


@register.filter
def pdate_year_month(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalaliyearmonth(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value


@register.filter
def pdate_year_month_day(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalaliyearmonthday(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value


@register.filter
def show_m2m(value):
    return u', '.join([str(d) for d in value.all()])


@register.filter
def filename(file_val):
    import os

    return os.path.basename(file_val.name)


@register.filter
def get_verbose_name_by_name(instance, name):
    return instance._meta.get_field_by_name(name)[0].verbose_name


@register.filter(is_safe=True)
def filesizeformat_persian(bytes):
    try:
        filesize_number_format = lambda value: formats.number_format(round(value, 1), 1)

        KB = 1 << 10
        MB = 1 << 20
        GB = 1 << 30
        TB = 1 << 40
        PB = 1 << 50

        if bytes < KB:
            value = "%s بایت" % filesize_number_format(bytes / KB)
        elif bytes < MB:
            value = "%s کیلوبایت" % filesize_number_format(bytes / KB)
        elif bytes < GB:
            value = "%s مگابایت" % filesize_number_format(bytes / MB)
        elif bytes < TB:
            value = "%s گیگابایت" % filesize_number_format(bytes / GB)
        elif bytes < PB:
            value = "%s ترابایت" % filesize_number_format(bytes / TB)
        else:
            value = "%s پنتابایت" % filesize_number_format(bytes / PB)

        return avoid_wrapping(value)
    except:
        return 0


@register.filter
def tostringrate(value):
    return str(int(value))


@register.filter
def get_range(value):
    return range(value)


@register.filter
def discount(val1, val2):
    return val1 - val2


@register.filter
def to_int(val):
    try:
        return int(val)
    except:
        return val


@register.filter
def get_years(val):
    try:
        val = int(val)
        year = int(gregorian_to_jalaliyear(datetime.date.today()))
        res = []
        for i in range(val):
            res.append(year - i)
        res = reversed(res)
        return res
    except:
        return []


@register.filter
def get_messages_count(user):
    return Notification.notify_count(user)


@register.filter
def upgrade_manager_count(user):
    return PermissionController.get_queryset(user, PermissionController.UPGRADE_MANAGER_PERM).count()

@register.filter
def max_str(val, size):
    if not val:
        return val
    if len(str(val)) > size:
        return str(val)[:size] + "..."
    else:
        return str(val)