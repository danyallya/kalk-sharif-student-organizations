from django_select2.fields import AutoModelSelect2Field

from document.models import BackupPackage
from experience.models import Experience
from home.models import HomeExp, HomePackage
from utils.forms import BaseModelForm

__author__ = 'M.Y'


class ExperienceChoiceField(AutoModelSelect2Field):
    queryset = Experience.objects
    search_fields = ['title__icontains']
    to_field = 'title'

    def get_model_field_values(self, value):
        return {'title': value}


class HomeExpForm(BaseModelForm):
    class Meta:
        model = HomeExp
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(HomeExpForm, self).__init__(*args, **kwargs)
        self.fields['experience'] = ExperienceChoiceField(required=True, label="تجربه")


class PackageChoiceField(AutoModelSelect2Field):
    queryset = BackupPackage.objects
    search_fields = ['title__icontains']
    to_field = 'title'

    def get_model_field_values(self, value):
        return {'title': value}


class HomePackageForm(BaseModelForm):
    class Meta:
        model = HomePackage
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(HomePackageForm, self).__init__(*args, **kwargs)
        self.fields['package'] = PackageChoiceField(required=True, label="بسته")
