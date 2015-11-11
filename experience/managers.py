# -*- coding: utf-8 -*-
from django.template.defaultfilters import striptags
from account.models import Organization
from account.permissions import PermissionController

from experience.actions import AddExperience, EditExperience
from experience.forms import ExperienceForm
from experience.models import Experience, Tag, University
from utils.forms import create_titled_filter, create_model_form
from utils.manager.action import AddAction, EditAction, ShowAction, DeleteAction, DoAction
from utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'

TagForm = create_model_form(Tag)
UniversityForm = create_model_form(University)
OrganizationForm = create_model_form(Organization)


class ExperienceManager(ObjectsManager):
    manager_name = u"experience_manager"
    manager_verbose_name = "تجربه ها"
    filter_form = create_titled_filter(Experience)
    actions = [
        AddExperience(),
        EditExperience(),
        ShowAction(ExperienceForm, height='350'),
        DeleteAction(),
    ]

    def get_all_data(self):
        return PermissionController.get_queryset(self.http_request.user, PermissionController.EXP_MANAGER_PERM)

    def can_view(self):
        return PermissionController.has_permission(self.http_request.user, PermissionController.EXP_MANAGER_PERM)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('body', u"متن", 17, True),
            ManagerColumn('university', u"دانشگاه", 5),
            ManagerColumn('organization', u"تشکل", 5),
            ManagerColumn('visitor_count', u"بازدید", 3),
            ManagerColumn('image_count', u"عکس", 3),
            ManagerColumn('comment_count', u"نظر", 3),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('last_change', u"تاریخ ویرایش", 3),
        ]
        return columns

    def get_body(self, obj):
        body = striptags(obj.content).replace('\r\n', ' ').replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
        if len(body) > 45:
            body = body[:45] + ' ...'
        return body

    def get_excel_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('body', u"متن", 20, True),
            ManagerColumn('creator', u"نویسنده", 7),
            ManagerColumn('university', u"دانشگاه", 7),
            ManagerColumn('organization', u"تشکل", 7),
            ManagerColumn('service', u"سرویس", 9),
            ManagerColumn('created_on', u"تاریخ ایجاد", 6),
            ManagerColumn('last_change', u"تاریخ ویرایش", 6),
        ]
        return columns


def confirm_obj(http_request, selected_instances):
    for p in selected_instances:
        p.confirm = True
        p.save()


class TagManager(ObjectsManager):
    manager_name = u"tag_manager"
    manager_verbose_name = "تگ ها"
    filter_form = create_titled_filter(Tag)
    actions = [
        AddAction(TagForm),
        EditAction(TagForm),
        ShowAction(TagForm, height='350'),
        DeleteAction(),
        DoAction(do_function=confirm_obj, action_name='confirm', action_verbose_name="تایید",
                 confirm_message="آیا از تایید موارد انتخاب شده اطمینان دارید؟")
    ]

    def get_all_data(self):
        return Tag.objects.filter()

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('confirm', u"تاییدشده", 3),
            ManagerColumn('creator', u"سازنده", 3),
            ManagerColumn('modifier', u"ویرایش کننده", 3),
        ]
        return columns


class UniversityManager(ObjectsManager):
    manager_name = u"university_manager"
    manager_verbose_name = "دانشگاه ها"
    filter_form = create_titled_filter(University)
    actions = [
        AddAction(UniversityForm),
        EditAction(UniversityForm),
        ShowAction(UniversityForm, height='350'),
        DeleteAction(),
        DoAction(do_function=confirm_obj, action_name='confirm', action_verbose_name="تایید",
                 confirm_message="آیا از تایید موارد انتخاب شده اطمینان دارید؟")
    ]

    def get_all_data(self):
        return University.objects.filter()

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('male_organizer', u"مسئول برادر", 7),
            ManagerColumn('female_organizer', u"مسئول خواهر", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('confirm', u"تاییدشده", 3),
            ManagerColumn('creator', u"سازنده", 3),
            ManagerColumn('modifier', u"ویرایش کننده", 3),
        ]
        return columns


class OrganizationManager(ObjectsManager):
    manager_name = u"organization_manager"
    manager_verbose_name = "تشکل ها"
    filter_form = create_titled_filter(Organization)
    actions = [
        AddAction(OrganizationForm),
        EditAction(OrganizationForm),
        ShowAction(OrganizationForm, height='350'),
        DeleteAction(),
        DoAction(do_function=confirm_obj, action_name='confirm', action_verbose_name="تایید",
                 confirm_message="آیا از تایید موارد انتخاب شده اطمینان دارید؟")
    ]

    def get_all_data(self):
        return Organization.objects.filter()

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('male_organizer', u"مسئول برادر", 7),
            ManagerColumn('female_organizer', u"مسئول خواهر", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('confirm', u"تاییدشده", 3),
            ManagerColumn('creator', u"سازنده", 3),
            ManagerColumn('modifier', u"ویرایش کننده", 3),
        ]
        return columns
