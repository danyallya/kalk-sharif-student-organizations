from django.utils.encoding import force_text
from account.permissions import PermissionController

from comment.models import ThreadedComment
from utils.forms import BaseModelForm
from utils.manager.action import DeleteAction, EditAction, DoAction
from utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class CommentForm(BaseModelForm):
    class Meta:
        model = ThreadedComment
        exclude = ('user', 'object_pk', 'content_type', 'parent', 'last_child')


def confirm_comment(http_request, selected_instances):
    for comment in selected_instances:
        comment.active = True
        comment.save()


class CommentManager(ObjectsManager):
    manager_name = u"comment_manager"
    manager_verbose_name = "نظر ها"
    actions = [
        EditAction(CommentForm),
        DeleteAction(),
        DoAction(do_function=confirm_comment, action_name='confirm_comment', action_verbose_name="تایید",
                 confirm_message="آیا از تایید دیدگاه های انتخاب شده اطمینان دارید؟")
    ]

    def get_all_data(self):
        return ThreadedComment.objects.filter()

    def can_view(self):
        return PermissionController.is_admin(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('id', u"شماره", 2),
            ManagerColumn('user', u"کاربر", 7),
            ManagerColumn('main_obj', u"موضوع", 7, True),
            ManagerColumn('body', u"متن", 20, True),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('active', u"تاییدشده", 3),
        ]
        return columns

    def get_main_obj(self, obj):
        try:
            return obj.content_type.name + "-" + force_text(
                obj.content_type.model_class().objects.get(id=obj.object_pk))
        except:
            return "---"

    def get_body(self, obj):
        body = obj.text.replace('\r\n', ' ').replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
        if len(body) > 45:
            body = body[:45] + ' ...'
        return body
