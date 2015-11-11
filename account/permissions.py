from django.http.response import HttpResponseForbidden

from account.models import Account, UpgradeMemberRequest
from document.models import Document, BackupPackage
from experience.models import Experience
from utils.models import PublishLeveled

__author__ = 'M.Y'


class Permission(object):
    def __init__(self, user):
        self.user = user

    def check(self):
        pass

    def get_queryset(self):
        pass


class ExperiencePermission(Permission):
    # PERMISSION TO SEE EXPERIENCE LIST AND SPECIFY QUERYSET THAT MUST SHOW TO USER
    def check(self):
        return True

    def get_queryset(self):
        if self.user.level >= Account.ORGANIZER_LEVEL:
            return Experience.objects.filter(confirm=True)
        elif self.user.level == Account.ACTIVE_LEVEL:
            return Experience.objects.filter(confirm=True).filter(publish_type__lte=PublishLeveled.ACTIVE_USERS_PUBLISH)
        else:
            return Experience.objects.filter(confirm=True).filter(publish_type=PublishLeveled.PUBLIC_PUBLISH)


class ExperienceManagerPermission(Permission):
    # PERMISSION TO MANAGE SOME EXPERIENCES IN OWN DASHBOARD - ALSO PERMISSION TO ADD NEW EXPERIENCE
    def check(self):
        return self.user.is_authenticated()

    def get_queryset(self):
        if self.user.level >= Account.BACKUP_MASTER:
            return Experience.objects.filter()
        elif self.user.level == Account.ORGANIZER_LEVEL:
            return Experience.objects.filter(organization=self.user.organization, university=self.user.university)
        elif self.user.level <= Account.ACTIVE_LEVEL:
            return Experience.objects.filter(creator=self.user)


class UserManagerPermission(Permission):
    # PERMISSION TO MANAGER SOME USER
    def check(self):
        return self.user.level >= Account.ORGANIZER_LEVEL

    def get_queryset(self):
        if self.user.level >= Account.BACKUP_MASTER:
            return Account.objects.filter()
        elif self.user.level == Account.ORGANIZER_LEVEL:

            organization_id = self.user.organization.id
            university_id = self.user.university.id

            return Account.objects \
                .filter(organization_members__organization_id=organization_id,
                        organization_members__university_id=university_id) \
                .exclude(id=self.user.id)
        else:
            return Account.objects.none()


class UpgradePermission(Permission):
    # PERMISSION TO USE THE UPGRADE USER LEVEL MODULE
    def check(self):
        return self.user.level < Account.ACTIVE_LEVEL


class UpgradeManagerPermission(Permission):
    def check(self):
        return self.user.level >= Account.ORGANIZER_LEVEL

    def get_queryset(self):
        if self.user.level >= Account.BACKUP_MASTER:
            return UpgradeMemberRequest.objects.filter(state__lt=UpgradeMemberRequest.STATE_REJECT)
        elif self.user.level == Account.ORGANIZER_LEVEL:
            return UpgradeMemberRequest.objects.filter(organization=self.user.organization,
                                                       state__lt=UpgradeMemberRequest.STATE_REJECT)


class DocumentPermission(Permission):
    # PERMISSION TO SEE DOCUMENT LIST AND SPECIFY QUERYSET THAT MUST SHOW TO USER
    def check(self):
        return True

    def get_queryset(self):
        if self.user.level >= Account.ORGANIZER_LEVEL:
            return Document.objects.filter()
        elif self.user.level == Account.ACTIVE_LEVEL:
            return Document.objects.filter().filter(publish_type__lte=PublishLeveled.ACTIVE_USERS_PUBLISH)
        else:
            return Document.objects.filter().filter(publish_type=PublishLeveled.PUBLIC_PUBLISH)


class PackagePermission(Permission):
    # PERMISSION TO SEE PACKAGE LIST AND SPECIFY QUERYSET THAT MUST SHOW TO USER
    def check(self):
        return True

    def get_queryset(self):
        if self.user.level >= Account.ORGANIZER_LEVEL:
            return BackupPackage.objects.filter(confirm=True)
        elif self.user.level == Account.ACTIVE_LEVEL:
            return BackupPackage.objects.filter(confirm=True).filter(
                publish_type__lte=PublishLeveled.ACTIVE_USERS_PUBLISH)
        else:
            return BackupPackage.objects.filter(confirm=True).filter(publish_type=PublishLeveled.PUBLIC_PUBLISH)


class PermissionController(object):
    EXP_PERM = ExperiencePermission
    DOC_PERM = DocumentPermission
    PACKAGE_PERM = PackagePermission
    EXP_MANAGER_PERM = ExperienceManagerPermission
    USER_PERM = UserManagerPermission
    UPGRADE_PERM = UpgradePermission
    UPGRADE_MANAGER_PERM = UpgradeManagerPermission

    @staticmethod
    def has_permission(user, perm):
        return perm(user).check()

    @staticmethod
    def get_queryset(user, perm):
        return perm(user).get_queryset()

    @staticmethod
    def is_active_user(user):
        if user.is_authenticated() and user.level >= Account.ACTIVE_LEVEL:
            return True
        return False

    @staticmethod
    def is_admin(user):
        if user.is_authenticated() and user.level >= Account.ADMIN_LEVEL:
            return True
        return False


# DECORATOR FOR CHECK PERMISSION TO ACCESS DJANGO VIEW
def permission_required(perm):
    def permission_decorator(view):
        def wrapper(request, *args, **kwargs):
            if PermissionController.has_permission(request.user, perm):
                return view(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

        return wrapper

    return permission_decorator
