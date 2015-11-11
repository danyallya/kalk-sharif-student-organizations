import json

__author__ = 'M.Y'

HELP_CASE_CHOICES = (
    # BASE
    ('logo', 'کل سایت | لوگو کالک'),
    ('header-map-first', 'کل سایت | نقشه سایت 1'),
    ('header-map-second', 'کل سایت | نقشه سایت 2'),
    ('header-map-third', 'کل سایت | نقشه سایت 3'),

    # EXPERIENCE
    ('send-image-header', 'تجربه | ارسال تصاویر شما'),
    ('experience-share-header', 'تجربه | معرفی به دیگران'),
    ('experience-complement-header', 'تجربه | تکمیل این تجربه'),
    ('experience-comments-panel', 'تجربه | پرسش و پاسخ'),
    ('experience-title', 'تجربه | عنوان تجربه'),
    ('experience-uni', 'تجربه | دانشگاه تجربه'),
    ('experience-author', 'تجربه | نویسنده تجربه'),
    ('experience-date', 'تجربه | تاریخ تجربه'),
    ('experience-content', 'تجربه | متن تجربه'),
    ('experience-right-title', 'تجربه | عنوان سمت راست تجربه'),
    ('experience-image', 'تجربه | عکس تجربه'),
    ('text-attachment', 'تجربه | متن ضمیمه'),
    ('video-attachment', 'تجربه | ویدیو ضمیمه'),
    ('link-attachment', 'تجربه | لینک ضمیمه'),
    ('image-attachment', 'تجربه | تصویر ضمیمه'),
    ('experience-related-ex', 'تجربه | تجربیات مرتبط'),
    ('experience-content', 'تجربه | متن تجربه'),
    ('experience-extra-images', 'تجربه | عکس های تجربه'),
    ('send-image-div', 'تجربه | بارگزاری تصویرهای شما'),
    ('show-all-images', 'تجربه | مشاهده همه تصاویر'),
    ('experience-rating', 'سند | امتیازدهی'),

    # DOCUMENT
    ('doc-action-map', 'سند | دریافت نقشه عملیاتی'),
    ('doc-your-experience', 'سند | تجربه شما'),
    ('doc-help', 'سند | راهنما'),
    ('doc-page-tree', 'سند | درختی سند'),
    ('doc-content', 'سند | متن سند'),
    ('doc-reference-tab', 'سند | تجربیات ارجاع شده'),
    ('doc-comments-tab', 'سند | دیدگاه ها و نظرات'),
    ('comments_link', 'سند | دیدگاه'),
    ('refs_link', 'سند | ارجاع'),
    ('document-rating', 'سند | امتیازدهی'),
)

__help_dict = None


def provide_help_instances(instances):
    global __help_dict
    __help_dict = {}

    for obj in instances:
        __help_dict[obj.code] = obj.text


def get_help_dict():
    if not __help_dict:
        from utils.models import HelpCase

        provide_help_instances(HelpCase.objects.all())
    return __help_dict


def context_provider(request):
    help_dict = get_help_dict()

    result = {'help': json.dumps(help_dict)}

    return result
