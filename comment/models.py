from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields import GenericIPAddressField
from account.models import Account

PATH_SEPARATOR = '/'
PATH_DIGITS = 10


class ThreadedComment(models.Model):
    user = models.ForeignKey(Account, verbose_name="کاربر", null=True, blank=True)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name='content type',
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.IntegerField('Object ID')
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    text = models.TextField(null=True)

    parent = models.ForeignKey('ThreadedComment', null=True, blank=True, default=None, related_name='children')
    last_child = models.ForeignKey('ThreadedComment', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='Last child')
    tree_path = models.TextField('Tree path', editable=False, db_index=True)

    active = models.BooleanField(verbose_name="تاییدشده", default=False)

    user_name = models.CharField("نام", max_length=255, null=True, blank=True)
    university_name = models.CharField("نام دانشگاه", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ('tree_path',)

    def __str__(self):
        return "%s: %s..." % (self.user.username, self.text[:50])

    @staticmethod
    def get_comment_count(content_type, obj_id):
        return ThreadedComment.objects.filter(content_type=content_type, object_pk=obj_id).count()

    @property
    def depth(self):
        return len(self.tree_path.split(PATH_SEPARATOR))

    @property
    def root_id(self):
        return int(self.tree_path.split(PATH_SEPARATOR)[0])

    @property
    def root_path(self):
        return ThreadedComment.objects.filter(pk__in=self.tree_path.split(PATH_SEPARATOR)[:-1])

    def save(self, *args, **kwargs):

        skip_tree_path = kwargs.pop('skip_tree_path', False)

        super(ThreadedComment, self).save(*args, **kwargs)
        try:
            self.content_type.model_class().objects.get(id=self.object_pk).update()
        except:
            pass

        if skip_tree_path:
            return None

        tree_path = str(self.pk).zfill(PATH_DIGITS)
        if self.parent:
            tree_path = PATH_SEPARATOR.join((self.parent.tree_path, tree_path))

            self.parent.last_child = self
            ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=self)

        self.tree_path = tree_path
        ThreadedComment.objects.filter(pk=self.pk).update(tree_path=self.tree_path)

    def delete(self, *args, **kwargs):
        # Fix last child on deletion.
        if self.parent_id:
            prev_child_id = ThreadedComment.objects.filter(parent=self.parent_id).exclude(pk=self.pk).order_by(
                '-submit_date').values_list('pk', flat=True)[0]
            ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=prev_child_id)
        obj = self.content_type.model_class().objects.get(id=self.object_pk)
        super(ThreadedComment, self).delete(*args, **kwargs)
        try:
            obj.update()
        except:
            pass


class UserRate(models.Model):
    content_type = models.ForeignKey(ContentType,
                                     verbose_name='content type',
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.IntegerField('Object ID')
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    user = models.ForeignKey(Account, verbose_name="کاربر", null=True, blank=True)
    ip_address = GenericIPAddressField()
    rate = models.IntegerField()

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازها"

    def __str__(self):
        return "%s: %s" % (self.user.username, self.created_on)

    def save(self, *args, **kwargs):
        super(UserRate, self).save(args, kwargs)
        try:
            self.content_type.model_class().objects.get(id=self.object_pk).update()
        except:
            pass

    def delete(self, using=None):
        obj = self.content_type.model_class().objects.get(id=self.object_pk)
        super(UserRate, self).delete(using)
        try:
            obj.update()
        except:
            pass
