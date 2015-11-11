# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory

from tinymce.widgets import TinyMCE

from account.models import Account
from account.permissions import PermissionController
from experience.models import Experience, ExperienceAttachment, Place, University
from utils.fields.select2 import UniversityChoiceField, OrganizationChoiceField, TagMultipleField
from utils.forms import BaseModelForm
from utils.models import ImageModel, Gallery

__author__ = 'M.Y'



# class TagMultipleField(TitledMultipleModelField):
#     queryset = Tag.objects


class ExperienceForm(BaseModelForm):
    class Meta:
        model = Experience
        exclude = ('gallery', 'attachments', 'image_cropping', 'uni_temp', 'creator_old', 'visitor_count',
                   'comment_count', 'rate')
        fields = ('title', 'publish_type', 'image', 'date', 'service', 'content', 'uni_state', 'uni_type', 'university',
                  'organization', 'tags')

    uni_state = forms.ModelChoiceField(queryset=Place.objects.all(), label="استان")
    uni_type = forms.ChoiceField(choices=University.UNI_TYPES, label="نوع دانشگاه")

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)

        # if self.instance.id:
        #     tag_queryset = Tag.objects.filter(Q(confirm=True) | Q(experiences__id=self.instance.id))
        # else:
        #     tag_queryset = Tag.objects.filter(confirm=True)
        self.fields['tags'] = TagMultipleField(required=False, label="تگ ها")

        self.fields['university'] = UniversityChoiceField(required=True, label="دانشگاه",
                                                          http_request=self.http_request)
        self.fields['organization'] = OrganizationChoiceField(required=True, label="تشکل",
                                                              http_request=self.http_request)

        if self.instance and self.instance.university:
            self.fields['uni_state'].initial = self.instance.university.state
            self.fields['uni_type'].initial = self.instance.university.uni_type

        self.fields['content'].widget = TinyMCE(attrs={'cols': 100, 'rows': 20}, mce_attrs={
            'force_br_newlines': False,
            'force_p_newlines': False,
            'forced_root_block': '',
            'width': "70%",
            'height': "300",
            'plugins': "fullpage",
            'toolbar': "fullpage",
            'verify_html': False,
            'cleanup': False
        })
        if (self.http_request.user.level < Account.ORGANIZER_LEVEL or not self.instance.id) \
                and 'confirm' in self.fields:
            del self.fields['confirm']

        if self.http_request.user.level < Account.ACTIVE_LEVEL and 'publish_type' in self.fields:
            del self.fields['publish_type']

            # self.fields['created_on'] = forms.DateField(label=u"تاریخ ایجاد")
            # self.fields['created_on'].initial = self.instance.created_on
            # self.fields['content'].widget = TinyMCE(attrs={'cols': 60, 'rows': 20})

    def save(self, commit=True):
        is_new = self.instance.id is None
        obj = super(ExperienceForm, self).save()

        if is_new:
            if PermissionController.is_active_user(self.http_request.user):
                obj.confirm = True

        obj.save()
        return obj


class SendImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ('image',)


class ImageForm(BaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = ImageModel
        exclude = ('gallery',)


class AttachmentForm(BaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = ExperienceAttachment
        exclude = ('experience',)


ImageFormset = inlineformset_factory(Gallery, ImageModel, form=ImageForm, extra=1, can_delete=True)
AttachmentFormset = inlineformset_factory(Experience, ExperienceAttachment, form=AttachmentForm,
                                          extra=1, can_delete=True)
