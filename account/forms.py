# -*- coding: utf-8 -*-
from collections import OrderedDict

from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django_select2.fields import AutoModelSelect2Field

from account.models import Account, UpgradeMemberRequest, Notification
from account.permissions import PermissionController
from experience.models import University, Place
from utils.fields.select2 import UniversityChoiceField, OrganizationChoiceField, RoleChoiceField
from utils.forms import BaseModelForm

__author__ = 'M.Y'


class SignUpForm(BaseModelForm):
    class Meta:
        model = Account
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(required=True, label=u"رمز عبور", widget=forms.PasswordInput)
        self.fields['re_password'] = forms.CharField(required=True, label=u"تکرار رمز عبور", widget=forms.PasswordInput)
        self.fields['captcha'] = CaptchaField(label=u"کد امنیتی", error_messages={
            'invalid': u"کد امنیتی وارد شده صحیح نمی باشد."},
                                              widget=CaptchaTextInput(attrs={'placeholder': u"کد امنیتی"}))

    def clean(self):
        cd = super(SignUpForm, self).clean()
        email = cd.get('email')
        username = cd.get('username')
        password = cd.get('password')
        re_password = cd.get('re_password')
        if (password or re_password) and password != re_password:
            self.errors['password'] = self.error_class([u'رمز عبور با تکرار آن مطابقت ندارد.'])
        try:
            if self.instance.id:
                Account.objects.exclude(id=self.instance.id).get(username=username)
            else:
                Account.objects.get(username=username)
            self.errors['username'] = self.error_class([u'نام کاربری تکراری می باشد.'])
        except Account.DoesNotExist:
            pass
        try:
            if self.instance.id:
                Account.objects.exclude(id=self.instance.id).get(email=email)
            else:
                Account.objects.get(email=email)
            self.errors['email'] = self.error_class([u'پست الکترونیک تکراری می باشد.'])
        except Account.DoesNotExist:
            pass
        return cd

    def save(self, commit=True):
        obj = super(SignUpForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            obj.set_password(password)
        obj.save()
        return obj


class AccountForm(SignUpForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(required=False, label=u"رمز عبور جدید", widget=forms.PasswordInput)
        self.fields['re_password'] = forms.CharField(required=False, label=u"تکرار رمز عبور جدید",
                                                     widget=forms.PasswordInput)
        if 'captcha' in self.fields:
            del self.fields['captcha']


class ActiveAccountForm(AccountForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'gender', 'mobile', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super(ActiveAccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['mobile'].required = True


class UpgradeMemberForm(BaseModelForm):
    class Meta:
        model = UpgradeMemberRequest
        exclude = ('user', 'state')
        fields = ('first_name', 'last_name', 'gender', 'uni_state', 'uni_type', 'university', 'organization', 'role',
                  'enter_year', 'grade', 'is_organizer', 'mobile')

    uni_state = forms.ModelChoiceField(queryset=Place.objects.all(), label="استان")
    uni_type = forms.ChoiceField(choices=University.UNI_TYPES, label="نوع دانشگاه")

    def __init__(self, *args, **kwargs):
        super(UpgradeMemberForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.university:
            self.fields['uni_state'].initial = self.instance.university.state
            self.fields['uni_type'].initial = self.instance.university.uni_type

        self.fields['university'] = UniversityChoiceField(required=True, label="دانشگاه",
                                                          http_request=self.http_request)
        self.fields['organization'] = OrganizationChoiceField(required=True, label="تشکل",
                                                              http_request=self.http_request)
        self.fields['role'] = RoleChoiceField(required=True, label="حوزه فعالیت", http_request=self.http_request)

    def save(self, commit=True):
        is_new = self.instance.id is None
        obj = super(UpgradeMemberForm, self).save(commit=False)
        obj.user = self.http_request.user
        if not is_new:
            obj.state = UpgradeMemberRequest.STATE_CHANGED
        else:
            Notification.send_notify(
                obj.user, "درخواست ارتقا سطح کاربری",
                "درخواست شما برای ارتقای سطح کاربری ارسال شد و به زودی نتیجه برای شما ارسال می گردد.")
        obj.save()
        self.save_m2m()
        return obj


class ChangeMemberForm(BaseModelForm):
    class Meta:
        model = UpgradeMemberRequest
        exclude = ('user', 'state', 'first_name', 'last_name', 'gender', 'mobile')
        fields = ['uni_state', 'uni_type', 'university', 'organization', 'role', 'enter_year', 'is_organizer']

    uni_state = forms.ModelChoiceField(queryset=Place.objects.all(), label="استان")
    uni_type = forms.ChoiceField(choices=University.UNI_TYPES, label="نوع دانشگاه")

    def __init__(self, *args, **kwargs):
        super(ChangeMemberForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.university:
            self.fields['uni_state'].initial = self.instance.university.state
            self.fields['uni_type'].initial = self.instance.university.uni_type

        self.fields['university'] = UniversityChoiceField(required=True, label="دانشگاه",
                                                          http_request=self.http_request)
        self.fields['organization'] = OrganizationChoiceField(required=True, label="تشکل",
                                                              http_request=self.http_request)
        self.fields['role'] = RoleChoiceField(required=True, label="حوزه فعالیت", http_request=self.http_request)


class CheckUpgradeForm(UpgradeMemberForm):
    class Meta:
        model = UpgradeMemberRequest
        exclude = ('user', 'state')
        fields = ('first_name', 'last_name', 'gender', 'university', 'organization', 'role',
                  'enter_year', 'grade', 'is_organizer', 'mobile')

    def __init__(self, *args, **kwargs):
        super(UpgradeMemberForm, self).__init__(*args, **kwargs)
        if 'uni_state' in self.fields:
            del self.fields['uni_state']

        if 'uni_type' in self.fields:
            del self.fields['uni_type']

    def save(self, commit=True):
        obj = super(UpgradeMemberForm, self).save(commit)
        return obj


class AccountChoiceField(AutoModelSelect2Field):
    queryset = Account.objects
    search_fields = ['first_name__icontains', 'last_name__icontains', 'username__icontains', ]
    to_field = '__str__'

    def get_model_field_values(self, value):
        return {'title': value}


class NotificationForm(BaseModelForm):
    class Meta:
        model = Notification
        exclude = ('seen', 'auto_gen')

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields['receiver'] = AccountChoiceField(required=True, label="گیرنده")

    def save(self, commit=True):
        obj = super(NotificationForm, self).save(commit)
        obj.auto_gen = False
        obj.save()
        return obj


class AccountManagerForm(BaseModelForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name', 'mobile', 'level')

    def __init__(self, *args, **kwargs):
        super(AccountManagerForm, self).__init__(*args, **kwargs)
        if PermissionController.is_admin(self.http_request.user):
            self.fields['password'] = forms.CharField(required=False, label=u"تغییر رمز عبور",
                                                      widget=forms.PasswordInput,
                                                      help_text="در صورت خالی بودن رمز عبور تغییر نمیکند.")

    def save(self, commit=True):
        obj = super(AccountManagerForm, self).save(commit)
        password = self.cleaned_data.get('password')
        if password:
            obj.set_password(password)
        obj.save()
        return obj
