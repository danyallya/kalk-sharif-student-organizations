from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField
from image_cropping.templatetags.cropping import cropped_thumbnail

from utils.models import BaseModel, CreateLog, ModifyLog


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
