# -*- coding:utf-8 -*-
import threading
from urllib import request
from django.conf import settings

from django.core.mail.message import EmailMultiAlternatives
from account.models import Account

__author__ = 'M.Y'


class MessageServices(threading.Thread):
    from_email = u'kalk@gmail.com'
    admin_email = u'kalk@gmail.com'

    @staticmethod
    def send_forget_password(email):
        try:
            user = Account.objects.get(email=email)
            user.create_code()

            url = settings.SITE_URL + "/change_pass/?c=" + request.quote(user.code)
            message = u"""
                <div style="direction:rtl;font-family:tahoma;font-size:17px;">
                باسلام
                <br/>
شما درخواست فراموشی گذرواژه را ارسال کرده اید.
    <br/>
    با استفاده از لینک زیر می توانید گذرواژه جدید خود را دریافت نمایید.
                    <br/><br/>
                    <br/>
                    <a href="%s">%s</a>

                    <br/>
                    <br/>
                    <br/>
                    موفق باشید
                </div>
                """ % (url, url)
            msg = EmailMultiAlternatives(subject=u"تغییر گذرواژه در کالک", body='',
                                         from_email=MessageServices.from_email,
                                         to=[user.email])
            msg.attach_alternative(message, "text/html")
            msg.send()
        except Exception as s:
            print(s)
