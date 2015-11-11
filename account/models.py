import datetime
import random
import string
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.safestring import mark_safe

from utils.models import Certifiable, BaseModel, ModifyLog, CreateLog


class Account(AbstractUser):
    NORMAL_LEVEL = 1
    ACTIVE_LEVEL = 2
    ORGANIZER_LEVEL = 3
    BACKUP_MASTER = 4
    ADMIN_LEVEL = 5
    LEVELS = (
        (1, "عادی"),
        (2, "فعال"),
        (3, "مسئول تشکل"),
        (4, "استاد پشتیبان"),
        (5, "مدیر"),
    )
    GENDER_CHOICES = (
        (1, "برادر"),
        (2, "خواهر"),
    )
    # birth_date = models.DateField(verbose_name="تاریخ تولد", null=True)
    # image = models.ImageField(blank=True, null=True, upload_to='user_images/')
    level = models.IntegerField("سطح دسترسی", default=1, choices=LEVELS)
    gender = models.IntegerField("جنسیت", default=1, choices=GENDER_CHOICES)
    mobile = models.CharField("شماره موبایل", max_length=15, null=True, blank=True,
                              validators=[
                                  RegexValidator(
                                      regex='^09\d{9}$',
                                      message='شماره موبایل اشتباه است',
                                      code='invalid_mobile'
                                  ),
                              ])
    code = models.CharField(u"کد فراموشی رمز عبور", max_length=200, null=True, blank=True)

    def __str__(self):
        if self.first_name:
            return self.get_full_name()
        return self.username

    def create_code(self):
        self.code = ''.join(
            random.choice(string.ascii_letters + string.digits + '(_)./,;][=+') for x in range(50))
        self.save()

    def get_current_organization_member(self):
        member_obj = self.organization_members.filter(expire_date__isnull=True)
        if member_obj:
            return member_obj[0]

    @property
    def organization(self):
        organization_member = self.get_current_organization_member()
        if organization_member:
            return organization_member.organization
        return None

    @property
    def university(self):
        organization_member = self.get_current_organization_member()
        if organization_member:
            return organization_member.university
        return None

    @property
    def role(self):
        organization_member = self.get_current_organization_member()
        if organization_member:
            return organization_member.role
        return None

    @property
    def grade(self):
        organization_member = self.get_current_organization_member()
        if organization_member:
            return organization_member.get_grade_display()
        return None

    @property
    def enter_year(self):
        organization_member = self.get_current_organization_member()
        if organization_member:
            return organization_member.enter_year
        return None

    @property
    def upgrade_request_state(self):
        try:
            instance = UpgradeMemberRequest.objects.get(user=self)
            return mark_safe(instance.form_state)
        except UpgradeMemberRequest.DoesNotExist:
            return None

    @property
    def notifications(self):
        return Notification.unseen_notifications(self).order_by('-id')

# SET DEFAULT ATTR FOR ANONYMOUS USER
setattr(AnonymousUser, 'notifications', [])
setattr(AnonymousUser, 'organization', None)
setattr(AnonymousUser, 'university', None)
setattr(AnonymousUser, 'level', 0)


class Organization(BaseModel, Certifiable):
    class Meta:
        verbose_name = "تشکل"
        verbose_name_plural = "تشکل ها"

    def get_male_organizers(self):
        return self.organization_members.filter(expire_date__isnull=True, user__gender=1, is_organizer=True)

    @property
    def male_organizer(self):
        res = self.get_male_organizers()
        return " - ".join([str(x.user) for x in res])

    def get_female_organizers(self):
        return self.organization_members.filter(expire_date__isnull=True, user__gender=2, is_organizer=True)

    @property
    def female_organizer(self):
        res = self.get_female_organizers()
        return " - ".join([str(x.user) for x in res])


class Role(BaseModel, Certifiable):
    class Meta:
        verbose_name = "حوزه فعالیت"
        verbose_name_plural = "حوزه های فعالیت"


class OrganizationMember(models.Model):
    GRADE_CHOICES = (
        (1, "کارشناسی"),
        (2, "کارشناسی ارشد"),
        (3, "دکتری"),
    )
    user = models.ForeignKey(Account, verbose_name="کاربر", related_name='organization_members')
    university = models.ForeignKey('experience.University', verbose_name="دانشگاه", related_name='organization_members')
    grade = models.IntegerField("مقطع تحصیلی", default=1, choices=GRADE_CHOICES)
    enter_year = models.CharField("سال ورود", max_length=10, null=True)
    organization = models.ForeignKey(Organization, verbose_name="تشکل", related_name='organization_members')
    is_organizer = models.BooleanField(verbose_name="آیا مسئول تشکل هستید؟", default=False)
    role = models.ForeignKey(Role, verbose_name="حوزه فعالیت", related_name='organization_members')

    expire_date = models.DateField(verbose_name="تاریخ اتمام", null=True, blank=True)

    class Meta:
        verbose_name = "عضویت در تشکل"
        verbose_name_plural = "عضویت ها در تشکل"

    def update(self, upgrade_request):
        if self.is_organizer and self.organization_id == upgrade_request.organization_id \
                and self.university_id == upgrade_request.university_id:
            self.grade = upgrade_request.grade
            self.enter_year = upgrade_request.enter_year
            self.role = upgrade_request.role
            self.is_organizer = upgrade_request.is_organizer
            self.save()
        else:
            print("ho")
            self.expire_date = datetime.date.today()
            self.save()
            upgrade_request.state = UpgradeMemberRequest.STATE_NEW
            upgrade_request.save()
            user = self.user
            user.level = Account.ACTIVE_LEVEL
            user.save()
            Notification.send_notify(user, "تغییر مشخصات تشکل", "درخواست تغییر مشخصات تشکل شما ارسال شد.")

    @staticmethod
    def create_from_request(upgrade_request):
        OrganizationMember.objects.create(user=upgrade_request.user, university=upgrade_request.university,
                                          grade=upgrade_request.grade, enter_year=upgrade_request.enter_year,
                                          organization=upgrade_request.organization, role=upgrade_request.role,
                                          is_organizer=upgrade_request.is_organizer)


class UpgradeMemberRequest(CreateLog, ModifyLog):
    user = models.OneToOneField(Account, verbose_name="کاربر")

    first_name = models.CharField("نام", max_length=300, null=True)
    last_name = models.CharField("نام خانوادگی", max_length=300, null=True)
    gender = models.IntegerField("جنسیت", default=1, choices=Account.GENDER_CHOICES)
    university = models.ForeignKey('experience.University', verbose_name="دانشگاه", null=True)
    grade = models.IntegerField("مقطع تحصیلی", default=1, choices=OrganizationMember.GRADE_CHOICES)

    ENTER_YEAR = [(1370 + i, 1370 + i) for i in range(25)]

    enter_year = models.IntegerField("سال ورود", null=True, choices=ENTER_YEAR)
    organization = models.ForeignKey(Organization, verbose_name="تشکل", null=True)
    is_organizer = models.BooleanField(verbose_name="آیا مسئول تشکل هستید؟", default=False)
    role = models.ForeignKey(Role, verbose_name="حوزه فعالیت", null=True)
    mobile = models.CharField("شماره موبایل", max_length=15, null=True)

    STATE_NEW = 1
    STATE_CHANGED = 2
    STATE_REJECT = 3
    STATE_ACCEPTED = 4
    STATE_CHOICES = (
        (1, "جدید"),
        (2, "ویرایش شده"),
        (3, "رد شده"),
        (4, "تایید شده"),
    )
    state = models.IntegerField("وضعیت", choices=STATE_CHOICES, default=1)

    class Meta:
        verbose_name = "درخواست ارتقا سطح کاربری"
        verbose_name_plural = "درخواست های ارتقا سطح کاربری"

    @property
    def form_state(self):
        if self.state == UpgradeMemberRequest.STATE_NEW:
            return "<span style='color:orange'>جدید</span>"
        elif self.state == UpgradeMemberRequest.STATE_REJECT:
            return "<span style='color:red'>رد شده</span>"
        elif self.state == UpgradeMemberRequest.STATE_CHANGED:
            return "<span style='color:orange'>ویرایش شده</span>"
        elif self.state == UpgradeMemberRequest.STATE_ACCEPTED:
            return "<span style='color:green'>تایید شده</span>"

    @staticmethod
    def get_for_user(account):
        try:
            request_instance = UpgradeMemberRequest.objects.get(user=account)
            request_instance.first_name = account.first_name
            request_instance.last_name = account.last_name
            request_instance.gender = account.gender
            request_instance.mobile = account.mobile
        except UpgradeMemberRequest.DoesNotExist:
            request_instance = UpgradeMemberRequest.objects.create(user=account,
                                                                   first_name=account.first_name,
                                                                   last_name=account.last_name,
                                                                   gender=account.gender,
                                                                   mobile=account.mobile,
                                                                   state=UpgradeMemberRequest.STATE_ACCEPTED)
        return request_instance


class Notification(BaseModel):
    receiver = models.ForeignKey(Account, verbose_name="گیرنده")
    seen = models.BooleanField(verbose_name="دیده شده", default=False)
    text = models.TextField(verbose_name="متن")
    auto_gen = models.BooleanField(verbose_name="پیام سیستمی", default=True)

    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان ها"

    @property
    def brief(self):
        if len(self.text) > 40:
            return self.text[:40] + " ..."
        return self.text

    @staticmethod
    def send_notify(user, title, text):
        return Notification.objects.create(receiver=user, title=title, text=text)

    @staticmethod
    def notify_count(user):
        return Notification.unseen_notifications(user).count()

    @staticmethod
    def unseen_notifications(user):
        return Notification.objects.filter(receiver=user, seen=False)

    @staticmethod
    def send_to_organizer(user, title, text):
        organization = user.organization
        if organization:
            if user.gender == 1:
                organizers = organization.get_male_organizers()
            else:
                organizers = organization.get_female_organizers()
            for organizer in organizers:
                Notification.send_notify(organizer, title, text)

    def set_seen(self):
        self.seen = True
        self.save()
