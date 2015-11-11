from account.permissions import PermissionController
from home.forms import HomePackageForm, HomeExpForm

from home.models import SliderItem, HomeExp, HomePackage
from utils.forms import create_model_form
from utils.manager.action import DeleteAction, EditAction, AddAction
from utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'

SliderForm = create_model_form(SliderItem)


class SliderManager(ObjectsManager):
    manager_name = u"slider_manager"
    manager_verbose_name = "اسلایدها"
    actions = [
        AddAction(SliderForm),
        EditAction(SliderForm),
        DeleteAction(),
    ]

    def get_all_data(self):
        return SliderItem.objects.filter()

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"کاربر", 7),
            ManagerColumn('body', u"متن", 20, True),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('active', u"فعال", 3),
        ]
        return columns

    def get_body(self, obj):
        body = obj.text.replace('\r\n', ' ').replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
        if len(body) > 45:
            body = body[:45] + ' ...'
        return body


class HomeExpManager(ObjectsManager):
    manager_name = u"home_exp_manager"
    manager_verbose_name = "تجربیات صفحه اول"
    actions = [
        AddAction(HomeExpForm),
        EditAction(HomeExpForm),
        DeleteAction(),
    ]

    def get_all_data(self):
        return HomeExp.objects.filter().select_related('experience')

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('experience', u"تجربه", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
        ]
        return columns


class HomePackageManager(ObjectsManager):
    manager_name = u"home_pack_manager"
    manager_verbose_name = "تجربیات صفحه اول"
    actions = [
        AddAction(HomePackageForm),
        EditAction(HomePackageForm),
        DeleteAction(),
    ]

    def get_all_data(self):
        return HomePackage.objects.filter().select_related('package')

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('package', u"بسته", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
        ]
        return columns
