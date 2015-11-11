from PIL import Image
from django.db import models

from utils.help_handler import HELP_CASE_CHOICES, provide_help_instances


class Titled(models.Model):
    title = models.CharField(verbose_name="عنوان", max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class CreateLog(models.Model):
    creator = models.ForeignKey('account.Account', verbose_name="سازنده", null=True, blank=True,
                                related_name='%(class)s_creators')
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        abstract = True


class ModifyLog(models.Model):
    modifier = models.ForeignKey('account.Account', verbose_name="ویرایش کننده", null=True, blank=True,
                                 related_name='%(class)s_modifiers')
    last_change = models.DateTimeField(verbose_name="تاریخ ویرایش", auto_now=True)

    class Meta:
        abstract = True


class BaseModel(Titled, CreateLog, ModifyLog):
    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Certifiable(models.Model):
    confirm = models.BooleanField(verbose_name="تاییدشده", default=False)

    class Meta:
        abstract = True


class PublishLeveled(models.Model):
    PUBLIC_PUBLISH = 1
    ACTIVE_USERS_PUBLISH = 2
    ORGANIZER_USERS_PUBLISH = 3

    PUBLISH_TYPES = (
        (PUBLIC_PUBLISH, "عمومی"),
        (ACTIVE_USERS_PUBLISH, "خاص اعضای فعال"),
        (ORGANIZER_USERS_PUBLISH, "خاص مسئول تشکل ها"),
    )

    publish_type = models.IntegerField(verbose_name="نوع انتشار", choices=PUBLISH_TYPES, default=1)

    class Meta:
        abstract = True


class VisitorTrack(models.Model):
    visitor_count = models.IntegerField("تعداد بازدید", default=0)

    class Meta:
        abstract = True

    def add_visit(self):
        self.visitor_count += 1
        self.save()

class Gallery(models.Model):
    def __str__(self):
        return "Gallery-%s" % self.id


class ImageModel(models.Model):
    image = models.ImageField(verbose_name="تصویر", upload_to="images/")
    gallery = models.ForeignKey(Gallery, verbose_name="گالری", related_name='images')
    confirm = models.BooleanField(verbose_name="تاییدشده", default=True)

    def __str__(self):
        return self.image.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ImageModel, self).save()
        image = Image.open(self.image)
        (width, height) = image.size
        size = (1024, int(1024 * height / width))
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)


class HelpCase(CreateLog, ModifyLog):
    code = models.CharField("عنصر", choices=HELP_CASE_CHOICES, unique=True, max_length=100)
    text = models.CharField("متن", max_length=500, default='')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "راهنما"
        verbose_name_plural = "راهنما ها"

    def save(self, *args, **kwargs):
        super(HelpCase, self).save(*args, **kwargs)
        provide_help_instances(HelpCase.objects.all())

    def delete(self, using=None):
        super(HelpCase, self).save(using)
        provide_help_instances(HelpCase.objects.all())
