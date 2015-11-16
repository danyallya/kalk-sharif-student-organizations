import os

from PIL import Image
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.aggregates import Sum
from django.utils.html import strip_tags
from image_cropping.fields import ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail
from comment.models import ThreadedComment, UserRate

from utils.models import BaseModel, Gallery, Certifiable, PublishLeveled, VisitorTrack


class Tag(BaseModel, Certifiable):
    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ ها"


class Place(BaseModel):
    class Meta:
        verbose_name = "محل"
        verbose_name_plural = "محل ها"


class University(BaseModel, Certifiable):
    UNI_TYPES = (
        (1, "دولتی"),
        (2, "آزاد"),
        (3, "پیام نور"),
        (4, "غیر انتفاعی"),
        (5, "علوم پزشکی"),
        (6, "فرهنگیان"),
        (7, "علمی-کاربردی"),
    )
    uni_type = models.IntegerField(verbose_name="نوع", choices=UNI_TYPES, null=True)
    state = models.ForeignKey(Place, verbose_name="استان", null=True)
    image = models.ImageField(verbose_name="تصویر", null=True, upload_to="university_image/")

    class Meta:
        verbose_name = "دانشگاه"
        verbose_name_plural = "دانشگاه ها"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(University, self).save()

    @property
    def male_organizer(self):
        res = self.organization_members.filter(expire_date__isnull=True, user__gender=1, is_organizer=True)
        return " - ".join([str(x.user) for x in res])

    @property
    def female_organizer(self):
        res = self.organization_members.filter(expire_date__isnull=True, user__gender=2, is_organizer=True)
        return " - ".join([str(x.user) for x in res])


class Experience(BaseModel, PublishLeveled, Certifiable, VisitorTrack):
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

    content = models.TextField(verbose_name="محتوا")
    date = models.DateField(verbose_name="تاریخ تجربه", null=True, blank=True)
    image = models.ImageField(verbose_name="تصویر", null=True, upload_to="experience_image/")
    # image_cropping = ImageRatioField('image', '128x292', help_text="", verbose_name="محدوده کراپ برای لیست")
    service = models.IntegerField(verbose_name="سرویس", choices=SERVICES, null=True)
    gallery = models.ForeignKey(Gallery, verbose_name="گالری", null=True)
    university = models.ForeignKey(University, verbose_name="دانشگاه", null=True)
    organization = models.ForeignKey('account.Organization', verbose_name="تشکل", null=True)
    tags = models.ManyToManyField(Tag, verbose_name="تگ ها", related_name='experiences')
    comment_count = models.IntegerField(verbose_name="تعداد کامنت ها", default=0)
    rate = models.FloatField(verbose_name="امتیاز", default=0)

    uni_temp = models.CharField(null=True, blank=True, max_length=255)
    creator_old = models.CharField(verbose_name="نویسنده", null=True, blank=True, max_length=255)

    class Meta:
        verbose_name = "تجربه"
        verbose_name_plural = "تجربه ها"

    def __str__(self):
        return "%s - %s" % (self.title, self.university.title)

    # @property
    # def cropped_image(self):
    #     return cropped_thumbnail(None, self, "image_cropping")

    @property
    def content_brief(self):
        content = strip_tags(self.content)
        if len(content) > 400:
            return content[:400] + ' ...'
        else:
            return content

    @property
    def image_count(self):
        return self.gallery.images.count() if self.gallery_id else 0

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

    def show_tags(self):
        return "  ".join([str(tag) for tag in self.tags.all()])

    def prepare_attachments(self):
        self.attach_images = []
        self.attach_video = []
        self.attach_text = []
        self.attach_link = []

        for attach in self.attachments.all():
            extension = attach.extension()
            if extension in EXTENSIONS['Image']:
                self.attach_images.append(attach)
            elif extension in EXTENSIONS['Video']:
                self.attach_video.append(attach)
            elif extension in EXTENSIONS['Document']:
                self.attach_text.append(attach)
            else:
                self.attach_link.append(attach)

        self.has_attach_images = bool(self.attach_text)
        self.has_attach_images = bool(self.attach_video) and not self.has_attach_images
        self.has_attach_images = bool(self.attach_images)
        self.has_attach_images = bool(self.attach_link)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Experience, self).save()

    def update(self):
        self.comment_count = ThreadedComment.objects.filter(content_type=ExperienceContentType,
                                                            object_pk=self.id).count()
        rates = UserRate.objects.filter(content_type=ExperienceContentType, object_pk=self.id)
        rate_count = rates.count()
        rate_sum = rates.aggregate(Sum('rate'))['rate__sum'] or 0
        self.rate = rate_sum / (rate_count or 1)
        self.save()

    @staticmethod
    def update_all():
        for obj in Experience.objects.all():
            obj.update()

    @staticmethod
    def get_last_experiences():
        return Experience.objects.filter(confirm=True, publish_type=PublishLeveled.PUBLIC_PUBLISH).order_by('-id')[:6]

    @staticmethod
    def get_visited_experiences():
        return Experience.objects.filter(confirm=True, publish_type=PublishLeveled.PUBLIC_PUBLISH).order_by(
            '-visitor_count')[:6]

    @staticmethod
    def get_rated_experiences():
        return Experience.objects.filter(confirm=True, publish_type=PublishLeveled.PUBLIC_PUBLISH).order_by('-rate')[:6]


try:
    ExperienceContentType = ContentType.objects.get_for_model(Experience)
except:
    ExperienceContentType = None

EXTENSIONS = {
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm', '.mp4'],
    'Audio': ['.mp3', '.wav', '.aiff', '.midi', '.m4p', '.wma']
}


class ExperienceAttachment(models.Model):
    attach = models.FileField(verbose_name="فایل", upload_to="experience_attachments/")
    experience = models.ForeignKey(Experience, related_name='attachments')

    def __str__(self):
        return self.attach.name

    def name(self):
        return os.path.basename(self.attach.name)

    def extension(self):
        name, extension = os.path.splitext(self.attach.name)
        return extension

    def get_type(self):
        extension = self.extension()
        if extension in EXTENSIONS['Image']:
            return 'image'
        elif extension in EXTENSIONS['Video']:
            return 'video'
        elif extension in EXTENSIONS['Document']:
            return 'doc'
        elif extension in EXTENSIONS['Audio']:
            return 'audio'
        else:
            return 'other'
