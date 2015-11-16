import os
import string
import random
import threading

from django.db import models
from django.conf import settings
from PyPDF2 import PdfFileReader
from django.template.defaultfilters import striptags
from image_cropping.templatetags.cropping import cropped_thumbnail

from wand.image import Image
from colorful.fields import RGBColorField
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Sum
from django.utils.encoding import smart_text

from image_cropping.fields import ImageRatioField, ImageCropField

from comment.models import ThreadedComment, UserRate
from experience.models import Experience
from utils.fields.file_fields import ContentTypeRestrictedFileField
from utils.models import BaseModel, PublishLeveled, Certifiable, CreateLog, ModifyLog, VisitorTrack


class Document(BaseModel, PublishLeveled, VisitorTrack):
    SERVICES = (
        (1, "شهدا و دفاع‌مقدس"),
        (2, "جهان اسلام و مستضعفین"),
        (3, "اردویی"),
        (4, "رشد و کادرسازی"),
        (5, "نقش آفرینی علمی"),
        (6, "مسائل تشکیلاتی"),
        (7, "جذب و ورودی جدید"),
        (8, "نقش آفرینی حاکمیتی"),
        (9, "رسانه و هنر"),
        (10, "آزادفکری"),
        (11, "جهادی"),
        (12, "مسجد و هیئت"),
    )
    ANIMATE_CHOICES = (
        (1, "از پایین"),
        (2, "از راست"),
        (3, "از چپ"),
    )
    image = ImageCropField(verbose_name="تصویر", null=True, upload_to="document_image/")
    tags = models.ManyToManyField('experience.Tag', verbose_name="تگ ها", related_name='documents', blank=True)
    file = models.FileField(verbose_name="نقشه عملیاتی", null=True, blank=True, upload_to='document_file/')
    intro = models.TextField("مقدمه", null=True, blank=True)
    list_text = models.TextField("متن صفحه اسناد", null=True, blank=True)
    service = models.IntegerField(verbose_name="سرویس", choices=SERVICES, null=True, default=1)
    animate_type = models.IntegerField(verbose_name="نوع انیمیشن", null=True, choices=ANIMATE_CHOICES, default=1)
    order = models.IntegerField(verbose_name="اولویت در لیست", null=True, default=1)
    image_cropping = ImageRatioField('image', '240x240', help_text="", verbose_name="محدوده کراپ برای لیست")
    comment_count = models.IntegerField(verbose_name="تعداد کامنت ها", default=0)
    rate = models.FloatField(verbose_name="امتیاز", default=0)
    color = RGBColorField(verbose_name="رنگ", default="#0b3f57")

    class Meta:
        verbose_name = "سند"
        verbose_name_plural = "سندها"

        # def save(self, *args, **kwargs):
        #     return super(Document, self).__init__(*args, **kwargs)
        # order = 1
        # for level in self.levels.filter(parent__isnull=True):
        #     level.order = order
        #     level.save()
        #     order += 1

    @property
    def animate_css_class(self):
        if self.animate_type == 1:
            return "bottom-info"
        elif self.animate_type == 2:
            return "right-info"
        else:
            return "left-info"

    @property
    def cropped_image(self):
        return cropped_thumbnail(None, self, "image_cropping")

    @property
    def text(self):
        return striptags(self.intro)[:200] if self.intro else ""

    @property
    def get_list_text(self):
        return striptags(self.list_text) if self.list_text else ""

    @property
    def ref_count(self):
        return Experience.objects.filter(document_levels__document=self).count()

    @property
    def intro_level(self):
        return DocumentLevel(id=0, title="مقدمه", text=self.intro, depth=1, color="#000000", parent=None, document=self)

    @property
    def service_icon(self):
        base_url = settings.STATIC_URL + 'images/services/'
        if self.service == 1:
            return base_url + "shohada.png"
        elif self.service == 2:
            return base_url + "jahaneeslam.png"
        elif self.service == 3:
            return base_url + "ordooyi.png"
        elif self.service == 4:
            return base_url + "roshd.png"
        elif self.service == 5:
            return base_url + "elmi.png"
        elif self.service == 6:
            return base_url + "tashkilati.png"
        elif self.service == 7:
            return base_url + "jazb.png"
        elif self.service == 8:
            return base_url + "naghshafarini.png"
        elif self.service == 9:
            return base_url + "resaneh.png"
        elif self.service == 10:
            return base_url + "azadfekri.png"
        elif self.service == 11:
            return base_url + "jahadi.png"
        elif self.service == 12:
            return base_url + "masjed.png"

    def update(self):
        self.comment_count = ThreadedComment.objects.filter(content_type=DocumentContentType, object_pk=self.id).count()
        rates = UserRate.objects.filter(content_type=DocumentContentType, object_pk=self.id)
        rate_count = rates.count()
        rate_sum = rates.aggregate(Sum('rate'))['rate__sum'] or 0
        self.rate = rate_sum / (rate_count or 1)
        self.save()

    @staticmethod
    def update_all():
        for doc in Document.objects.all():
            doc.update()


try:
    DocumentContentType = ContentType.objects.get_for_model(Document)
except:
    DocumentContentType = None


class SpecificDocument(CreateLog, ModifyLog):
    doc = models.OneToOneField('document.Document', verbose_name="سند", related_name='spec')

    class Meta:
        verbose_name = "سند برگزیده"
        verbose_name_plural = "اسناد برگزیده"


class DocumentLevel(BaseModel):
    document = models.ForeignKey('Document', verbose_name="سند", related_name='levels')
    parent = models.ForeignKey('DocumentLevel', verbose_name="دربرگیرنده", null=True, blank=True, default=None,
                               related_name='children', on_delete=models.CASCADE)
    text = models.TextField("متن", null=True, blank=True)
    color = RGBColorField(verbose_name="رنگ", default="#000000")
    depth = models.IntegerField("سطح", default=1)
    comment_count = models.IntegerField("تعداد دیدگاه ها", default=0)
    references = models.ManyToManyField('experience.Experience', verbose_name="تجربیات ارجاع شده",
                                        blank=True, related_name='document_levels')

    class Meta:
        verbose_name = "طبقه سند"
        verbose_name_plural = "طبقه های سند"

    @property
    def opacity(self):
        if self.depth == 1:
            return 1
        elif self.depth == 2:
            return 0.5
        elif self.depth == 3:
            return 0.3
        else:
            return 0.2

    @property
    def references_count(self):
        return self.references.count()

    def save(self, *args, **kwargs):
        if self.parent_id:
            self.color = self.parent.color
        if self.id:
            self.comment_count = ThreadedComment.objects.filter(content_type=DocumentLevelContentType,
                                                                object_pk=smart_text(self.id), active=True
                                                                ).count()
        super(DocumentLevel, self).save(*args, **kwargs)
        # order = 1
        for child in self.children.all():
            # child.order = order
            child.save()
            # order += 1


try:
    DocumentLevelContentType = ContentType.objects.get_for_model(DocumentLevel)
except:
    DocumentLevelContentType = None


class BackupPackage(BaseModel, PublishLeveled, Certifiable, VisitorTrack):
    document = models.ForeignKey(Document, verbose_name="سند", null=True, blank=True, related_name='packages')
    pdf_file = ContentTypeRestrictedFileField(
        verbose_name="فایل", null=True,
        upload_to='backup_package/',
        # content_types=['application/pdf'],
        # max_upload_size=5242880
    )
    image = models.ImageField(verbose_name="تصویر", null=True, upload_to="backup_package_image/", blank=True)
    tags = models.ManyToManyField('experience.Tag', verbose_name="تگ ها", related_name='backups', blank=True)
    receive_count = models.IntegerField(verbose_name="تعداد دانلود", default=0)
    rate = models.FloatField(verbose_name="امتیاز", default=0)
    # university = models.ForeignKey('experience.University', verbose_name="دانشگاه", null=True, default=1)

    cat = models.ForeignKey('document.PackageSubCat', verbose_name="دسته بندی", default=None, null=True)

    class Meta:
        verbose_name = "بسته پشتیبان"
        verbose_name_plural = "بسته های پشتیبان"

    @property
    def default_image(self):
        return "/static/images/page/pdf_package.png"

    @property
    def pack_image(self):
        if self.image:
            return self.image.url
        else:
            return self.default_image

    def save(self, *args, **kwargs):
        super(BackupPackage, self).save(*args, **kwargs)

    def rename(self):
        old_path = self.pdf_file.path

        new_name = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(17))
        self.pdf_file.name = 'backup_package/' + new_name + '.pdf'

        os.rename(old_path, self.pdf_file.path)

        self.save()

    def update(self):
        rates = UserRate.objects.filter(
            content_type=BackupPackageContentType,
            object_pk=self.id,
        )
        rate_count = rates.count()
        rate_sum = rates.aggregate(Sum('rate'))['rate__sum'] or 0
        self.rate = rate_sum / (rate_count or 1)
        self.save()

    @property
    def pdf_images(self):
        if not self.pdf_file:
            return []
        filepath = settings.MEDIA_ROOT + '/' + self.pdf_file.name
        input_file = PdfFileReader(open(filepath, 'rb'))
        output_dir = settings.MEDIA_URL + self.pdf_file.name + '_gif/'
        for i in range(input_file.getNumPages()):
            yield output_dir + str(i) + '.gif'

    # def convert_to_png(self, width=0, height=0):
    #     self.__convert_to_img__(width, height, 'png')
    #
    # def convert_to_jpg(self, width=0, height=0):
    #     self.__convert_to_img__(width, height, 'jpg')

    def pdf_update(self):
        try:
            Image(filename=self.pdf_file.name, resolution=140)
        except:
            self.rename()
            self.__convert_to_img__()

    def __convert_to_img__(self, width=0, height=0, format='gif'):
        ConvertPdfThread(self.pdf_file.name, width, height, format).start()


class PackageSubCat(BaseModel):
    CATEGORIES = (
        (1, "چندرسانه ای"),
        (2, "اساتید و اشخاص"),
        (3, "مکان یابی"),
        (4, "کتابخانه"),
        (5, "اردویی"),
        (6, "آیین نامه"),
    )
    cat = models.IntegerField(verbose_name="دسته بندی", default=1, choices=CATEGORIES)
    icon = models.ImageField(verbose_name="آیکن", upload_to="package_cat_icons/")

    class Meta:
        verbose_name = "دسته بسته پشتیبان"
        verbose_name_plural = "دسته های بسته پشتیبان"

    def __str__(self):
        return "%s - %s" % (self.get_cat_display(), self.title)

    @property
    def parent_icon(self):
        if self.cat == 1:
            return settings.STATIC_URL + 'images/media-h.png'
        elif self.cat == 2:
            return settings.STATIC_URL + 'images/teachers-h.png'
        elif self.cat == 3:
            return settings.STATIC_URL + 'images/location-h.png'
        elif self.cat == 4:
            return settings.STATIC_URL + 'images/lib.png'
        elif self.cat == 5:
            return settings.STATIC_URL + 'images/header-fun-h.png'
        elif self.cat == 6:
            return settings.STATIC_URL + 'images/rule-h.png'


class ConvertPdfThread(threading.Thread):
    def __init__(self, filename, width=0, height=0, format='gif'):
        threading.Thread.__init__(self)
        self.format = format
        self.height = height
        self.width = width
        self.filename = filename

    def run(self):
        size = ''
        if self.width and self.height:
            size = '_' + str(self.width) + 'x' + str(self.height) + 'px'

        if not self.filename:
            return

        filepath = settings.MEDIA_ROOT + '/' + self.filename
        output_dir = filepath + '_' + self.format + size + '/'
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

            input_file = PdfFileReader(open(filepath, 'rb'))
            for i in range(input_file.getNumPages()):
                with Image(filename=filepath + '[' + str(i) + ']', resolution=140) as img:
                    if len(size) > 0:
                        img.resize(self.width, self.height)
                    img.format = self.format
                    img.save(filename=output_dir + str(i) + '.' + self.format)


try:
    BackupPackageContentType = ContentType.objects.get_for_model(BackupPackage)
except:
    BackupPackageContentType = None
