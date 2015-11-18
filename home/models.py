from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField
from image_cropping.templatetags.cropping import cropped_thumbnail

from utils.models import BaseModel, CreateLog, ModifyLog, VisitorTrack


class SliderItem(BaseModel):
    image = ImageCropField(verbose_name="تصویر", null=True, upload_to="slider_image/")
    image_cropping = ImageRatioField('image', '1020x386', help_text="", verbose_name="محدوده کراپ")
    text = models.TextField(verbose_name="متن", null=True)
    link = models.URLField(verbose_name="لینک", null=True)
    active = models.BooleanField(verbose_name="فعال", default=True)

    class Meta:
        verbose_name = "اسلاید"
        verbose_name_plural = "اسلاید ها"

    @property
    def slide_image(self):
        return cropped_thumbnail(None, self, "image_cropping")


class HomeExp(CreateLog, ModifyLog):
    experience = models.OneToOneField('experience.Experience', verbose_name="تجربه")

    class Meta:
        verbose_name = "تجربیات صفحه اول"
        verbose_name_plural = "تجربیات صفحه اول"


class HomePackage(CreateLog, ModifyLog):
    package = models.OneToOneField('document.BackupPackage', verbose_name="بسته پشتیبان")

    class Meta:
        verbose_name = "تجربیات صفحه اول"
        verbose_name_plural = "تجربیات صفحه اول"


class HomeTV(BaseModel):
    text = models.TextField(verbose_name="متن", default="", blank=True)
    date = models.DateField(verbose_name="تاریخ", null=True, blank=True)
    image = models.ImageField(verbose_name="تصویر", null=True, upload_to="experience_image/")
    university = models.ForeignKey('experience.University', verbose_name="دانشگاه", null=True, blank=True)
    PLACE_CHOICES = (
        (1, "ویدیو اصلی"),
        (2, "ویدیو سمت چپ"),
        (3, "اسلایدر ویدیو"),
    )
    page_place = models.IntegerField(verbose_name="مکان در صفحه", null=True, blank=True)

    class Meta:
        verbose_name = "کالک TV صفحه اول"
        verbose_name_plural = "کالک TV صفحه اول"


class HomeSchool(BaseModel, VisitorTrack):
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
    image = models.ImageField(verbose_name="تصویر", null=True, upload_to="experience_image/")
    service = models.IntegerField(verbose_name="سرویس", choices=SERVICES, null=True)

    class Meta:
        verbose_name = "مدرسته کالک صفحه اول"
        verbose_name_plural = "مدرسته کالک صفحه اول"
