import json

from django.http.response import HttpResponse, Http404
from django.shortcuts import render

from django.utils.encoding import smart_text
from account.models import Notification

from comment.models import ThreadedComment
from comment.util import CommentHandler


def send_comment(request, content_type_id):
    obj_id = request.POST.get('id')
    text = request.POST.get('text')
    name = request.POST.get('name')
    uni_name = request.POST.get('uni_name')
    res = False
    content = ""
    if text:
        parent_id = request.POST.get('parent_id') or None
        comment = ThreadedComment(
            content_type_id=content_type_id,
            object_pk=smart_text(obj_id),
            text=text,
            user=request.user if not request.user.is_anonymous() else None,
            parent_id=parent_id,
        )

        if request.user.is_anonymous():
            comment.user_name = name
            comment.university_name = uni_name

        if not request.user.is_anonymous():
            comment.active = True
        else:
            comment.active = False
            Notification.send_to_organizer(request.user, "کامنت جدید", "یک کامنت تایید نشده جدید وجود دارد.")

        comment.save()

        res = True

        if comment.active:
            content = CommentHandler.render_comment_item(comment)

        message = "پیام شما با موفقیت ثبت شد."
    else:
        message = "متن نظر اجباری است."

    return HttpResponse(json.dumps({'res': res, 'message': message, 'content': content}), 'application/json')


def show_comments(request, content_type_id):
    obj_id = request.GET.get('id')
    if not obj_id:
        raise Http404
    return render(request, 'comments/show_comments.html',
                  {'obj_id': obj_id, 'content_type_id': content_type_id})


def comments_count(request, content_type_id):
    obj_id = request.GET.get('id')
    if not obj_id:
        raise Http404
    count = ThreadedComment.objects.filter(
        content_type_id=content_type_id,
        object_pk=smart_text(obj_id),
        active=True,
    ).count()
    return HttpResponse(json.dumps({'count': count}), 'application/json')
