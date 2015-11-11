from account.actions import CheckRequestAction
from account.forms import NotificationForm, AccountForm, AccountManagerForm
from account.models import Notification
from account.permissions import PermissionController
from utils.calverter import gregorian_to_jalali

from utils.manager.action import DeleteAction, EditAction, AddAction
from utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class AccountManager(ObjectsManager):
    manager_name = u"account_manager"
    manager_verbose_name = "کاربران"

    def __init__(self, http_request):
        super(AccountManager, self).__init__(http_request)
        if self.can_view():
            if PermissionController.is_admin(http_request.user):
                self.actions = [
                    AddAction(AccountManagerForm),
                    EditAction(AccountManagerForm),
                    DeleteAction(),
                ]
            else:
                self.actions = [
                    EditAction(AccountManagerForm),
                ]

    def get_all_data(self):
        return PermissionController.get_queryset(self.http_request.user, PermissionController.USER_PERM)

    def get_columns(self):
        columns = [
            ManagerColumn('username', u"نام کاربری", 3),
            ManagerColumn('first_name', u"نام", 7),
            ManagerColumn('last_name', u"نام خانوادگی", 7),
            ManagerColumn('university', u"دانشگاه", 7),
            ManagerColumn('organization', u"تشکل", 7),
            ManagerColumn('level', u"سطح دسترسی", 3),
            ManagerColumn('upgrade_request_state', u"درخواست ارتقا", 4, allow_html=True),
            ManagerColumn('date_joined', u"تاریخ ایجاد", 3),
        ]
        return columns

    def can_view(self):
        return PermissionController.has_permission(self.http_request.user, PermissionController.USER_PERM)

    def get_excel_columns(self):
        columns = [
            ManagerColumn('username', u"نام کاربری", 5),
            ManagerColumn('first_name', u"نام", 6),
            ManagerColumn('last_name', u"نام خانوادگی", 7),
            ManagerColumn('gender', u"جنسیت", 3),
            ManagerColumn('mobile', u"شماره موبایل", 6),
            ManagerColumn('level', u"سطح دسترسی", 5),
            ManagerColumn('university', u"دانشگاه", 7),
            ManagerColumn('organization', u"تشکل", 7),
            ManagerColumn('role', u"حوزه فعالیت", 7),
            ManagerColumn('grade', u"مقطع تحصیلی", 7),
            ManagerColumn('enter_year', u"سال ورود", 3),
            ManagerColumn('date_joined', u"تاریخ ایجاد", 5),
            ManagerColumn('last_login', u"آخرین ورود", 8, True),
        ]
        return columns

    def get_last_login(self, obj):
        time = obj.last_login.time()
        date = gregorian_to_jalali(obj.last_login)
        return "%s - %s" % (date, time.strftime("%H:%M"))


class UpgradeRequestManager(ObjectsManager):
    manager_name = u"upgrade_request_manager"
    manager_verbose_name = "درخواست های ارتقا سطح کاربری"
    actions = [
        CheckRequestAction(),
    ]

    def get_all_data(self):
        return PermissionController.get_queryset(self.http_request.user, PermissionController.UPGRADE_MANAGER_PERM)

    def can_view(self):
        return PermissionController.has_permission(self.http_request.user, PermissionController.UPGRADE_MANAGER_PERM)

    def get_columns(self):
        columns = [
            ManagerColumn('id', u"شماره", 2),
            ManagerColumn('first_name', u"نام", 7),
            ManagerColumn('last_name', u"نام خانوادگی", 7),
            ManagerColumn('university', u"دانشگاه", 7),
            ManagerColumn('organization', u"تشکل", 7),
            ManagerColumn('role', u"حوزه فعالیت", 7),
            ManagerColumn('state', u"وضعیت درخواست", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
        ]
        return columns


class NotificationManager(ObjectsManager):
    manager_name = u"message_manager"
    manager_verbose_name = "پیام ها"
    actions = [
        AddAction(NotificationForm, action_verbose_name="ارسال پیام جدید", form_title="ارسال پیام"),
        DeleteAction(),
    ]

    def get_all_data(self):
        return Notification.objects.filter(auto_gen=False).select_related('receiver')

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 5),
            ManagerColumn('brief', u"متن", 7),
            ManagerColumn('receiver', u"گیرنده", 5),
            ManagerColumn('seen', u"دیده شده", 2),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
        ]
        return columns
