import os

from django.forms.models import inlineformset_factory
from django_select2.fields import AutoModelSelect2MultipleField, AutoModelSelect2Field
from tinymce.widgets import TinyMCE

from account.models import Account
from account.permissions import PermissionController
from document.models import Document, DocumentLevel, BackupPackage, SpecificDocument, PackageSubCat
from experience.models import Experience
from utils.fields.select2 import TagMultipleField
from utils.forms import BaseModelForm, create_model_form
from utils.widgets.color import ColorHexFieldWidget

__author__ = 'M.Y'


class DocumentForm(BaseModelForm):
    class Meta:
        model = Document
        exclude = ('comment_count', 'rate', 'visitor_count')

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['tags'] = TagMultipleField(required=False, label="تگ ها")
        self.fields['intro'].widget = TinyMCE(attrs={'cols': 100, 'rows': 20}, mce_attrs={
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
        self.fields['list_text'].widget = TinyMCE(attrs={'cols': 100, 'rows': 20}, mce_attrs={
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

        if self.http_request.user.level < Account.ACTIVE_LEVEL and 'publish_type' in self.fields:
            del self.fields['publish_type']


class DocumentLevelForm(BaseModelForm):
    class Meta:
        model = DocumentLevel
        fields = ('title', 'text')

    def __init__(self, *args, **kwargs):
        super(DocumentLevelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = TinyMCE(attrs={'cols': 100, 'rows': 20}, mce_attrs={
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


class ExperienceChoiceField(AutoModelSelect2MultipleField):
    queryset = Experience.objects
    search_fields = ['title__icontains']
    to_field = 'title'

    def get_model_field_values(self, value):
        return {'title': value}


class DocumentFirstLevel(BaseModelForm):
    class Meta:
        model = DocumentLevel
        fields = ('title', 'text', 'color')

    def __init__(self, *args, **kwargs):
        super(DocumentFirstLevel, self).__init__(*args, **kwargs)
        self.fields['color'].widget = ColorHexFieldWidget()
        self.fields['text'].widget = TinyMCE(attrs={'cols': 100, 'rows': 20}, mce_attrs={
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


class DocumentSecondLevel(BaseModelForm):
    class Meta:
        model = DocumentLevel
        fields = ('title', 'text', 'references')

    def __init__(self, *args, **kwargs):
        super(DocumentSecondLevel, self).__init__(*args, **kwargs)
        self.fields['references'] = ExperienceChoiceField(required=False, label="تجربیات ارجاع شده")
        self.fields['text'].widget = TinyMCE(attrs={'cols': 100, 'rows': 20}, mce_attrs={
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


class DocumentThirdLevel(DocumentLevelForm):
    class Meta:
        model = DocumentLevel
        fields = ('title', 'text')


DocumentFirstLevelFormset = inlineformset_factory(Document, DocumentLevel, form=DocumentFirstLevel, can_delete=True)


class DocumentChoiceField(AutoModelSelect2Field):
    queryset = Document.objects
    search_fields = ['title__icontains']
    to_field = 'title'

    def get_model_field_values(self, value):
        return {'title': value}


class BackupPackageForm(BaseModelForm):
    class Meta:
        model = BackupPackage
        exclude = ('receive_count', 'rate', 'visitor_count')

    def __init__(self, *args, **kwargs):
        super(BackupPackageForm, self).__init__(*args, **kwargs)
        if 'tags' in self.fields:
            self.fields['tags'] = TagMultipleField(required=False, label="تگ ها")
        if 'document' in self.fields:
            self.fields['document'] = DocumentChoiceField(required=False, label="سند مربوطه")

        if (self.http_request.user.level < Account.ORGANIZER_LEVEL or not self.instance.id) \
                and 'confirm' in self.fields:
            del self.fields['confirm']

        if self.http_request.user.level < Account.ACTIVE_LEVEL and 'publish_type' in self.fields:
            del self.fields['publish_type']

        self.fields['cat'].queryset = PackageSubCat.objects.filter().order_by('title')

    def clean(self):
        cd = super(BackupPackageForm, self).clean()
        f = cd.get('pdf_file')
        ext = os.path.splitext(f.name)[1][1:].lower()
        if not ext == 'pdf':
            self.errors['pdf_file'] = "فقط فایل pdf مورد قبول می باشد."
        return cd

    def save(self, commit=True):
        is_new = self.instance.id is None
        obj = super(BackupPackageForm, self).save()

        if is_new:
            if PermissionController.is_active_user(self.http_request.user):
                obj.confirm = True

        obj.save()
        return obj


BackupPackageFormset = inlineformset_factory(Document, BackupPackage, form=BackupPackageForm,
                                             exclude=('document', 'receive_count', 'rate', 'tags', 'image'),
                                             extra=1, can_delete=True)


class SpecificDocumentForm(BaseModelForm):
    class Meta:
        model = SpecificDocument
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(SpecificDocumentForm, self).__init__(*args, **kwargs)
        self.fields['doc'] = DocumentChoiceField(required=True, label="سند")


PackageSubCatForm = create_model_form(PackageSubCat)
