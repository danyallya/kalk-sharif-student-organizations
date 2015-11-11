from account.permissions import PermissionController
from document.actions import AddDocument, EditDocument, EditLevelsAction, BackupPackageEdit
from document.forms import BackupPackageForm, SpecificDocumentForm, PackageSubCatForm
from document.models import Document, BackupPackage, SpecificDocument, PackageSubCat
from utils.forms import create_titled_filter
from utils.manager.action import DeleteAction, AddAction, EditAction, DoAction
from utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class DocumentManager(ObjectsManager):
    manager_name = u"document_manager"
    manager_verbose_name = "سند ها"
    filter_form = create_titled_filter(Document)
    actions = [
        AddDocument(),
        EditDocument(),
        DeleteAction(),
        EditLevelsAction(),
        BackupPackageEdit()
    ]

    def get_all_data(self):
        return Document.objects.filter()

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('visitor_count', u"بازدید", 3),
            ManagerColumn('comment_count', u"نظر", 3),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('last_change', u"تاریخ ویرایش", 3),
        ]
        return columns


def confirm_packages(http_request, selected_instances):
    for p in selected_instances:
        p.confirm = True
        p.save()


class BackupPackageManager(ObjectsManager):
    manager_name = u"backup_manager"
    manager_verbose_name = "بسته های پشتیبان"
    filter_form = create_titled_filter(BackupPackage)
    actions = [
        AddAction(BackupPackageForm),
        EditAction(BackupPackageForm),
        DeleteAction(),
        DoAction(do_function=confirm_packages, action_name='confirm_packages', action_verbose_name="تایید",
                 confirm_message="آیا از تایید دیدگاه های انتخاب شده اطمینان دارید؟")
    ]

    def get_all_data(self):
        return BackupPackage.objects.filter()

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 6),
            ManagerColumn('visitor_count', u"بازدید", 1),
            ManagerColumn('receive_count', u"دانلود", 1),
            ManagerColumn('cat', u"دسته", 5),
            ManagerColumn('created_on', u"تاریخ ایجاد", 2),
            ManagerColumn('last_change', u"تاریخ ویرایش", 2),
            ManagerColumn('confirm', u"تایید", 1),
        ]
        return columns


class PackageSubCatManager(ObjectsManager):
    manager_name = u"package_sub_manager"
    manager_verbose_name = "زیردسته بسته پشتیبان"
    actions = [
        AddAction(PackageSubCatForm),
        EditAction(PackageSubCatForm),
        DeleteAction(),
    ]

    def get_all_data(self):
        return PackageSubCat.objects.filter()

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('cat', u"دسته بندی", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
        ]
        return columns


class HomeExpManager(ObjectsManager):
    manager_name = u"spec_doc_manager"
    manager_verbose_name = "اسناد برگزیده"
    actions = [
        AddAction(SpecificDocumentForm),
        EditAction(SpecificDocumentForm),
        DeleteAction(),
    ]

    def get_all_data(self):
        return SpecificDocument.objects.filter().select_related('doc')

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('doc', u"سند", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
        ]
        return columns
