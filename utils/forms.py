# -*- coding:utf-8 -*-
from django import forms

from utils.date import handel_date_fields

__author__ = 'M.Y'


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(BaseForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        # process_js_validations(self)

    def clean(self):
        cd = super(BaseForm, self).clean()
        return cd


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(BaseModelForm, self).__init__(*args, **kwargs)
        if 'creator' in self.fields:
            del self.fields['creator']
        if 'modifier' in self.fields:
            del self.fields['modifier']
        handel_date_fields(self)
        # process_js_validations(self)

    def clean(self):
        cd = super(BaseModelForm, self).clean()
        return cd

    def save(self, commit=True):
        obj = super(BaseModelForm, self).save(commit=False)

        if hasattr(self, 'http_request'):
            if obj.id:
                obj.modifier = self.http_request.user
            else:
                obj.creator = self.http_request.user

        if commit:
            obj.save()
            self.save_m2m()

        return obj


class BaseFilterModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(BaseFilterModelForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        # process_js_validations(self)


def create_titled_filter(klass):
    class FilterForm(BaseFilterModelForm):
        class Meta:
            model = klass
            fields = ('title',)

    return FilterForm


def create_model_form(klass):
    class Form(BaseModelForm):
        class Meta:
            model = klass
            exclude = ()

    return Form
