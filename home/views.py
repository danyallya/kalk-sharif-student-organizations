from django.shortcuts import render
from account.permissions import PermissionController
from document.models import BackupPackage
from experience.models import Experience, University
from home.models import SliderItem, HomeExp, HomePackage


def home(request):
    slides = SliderItem.objects.all()

    experiences = Experience.objects.filter(
        id__in=HomeExp.objects.all().select_related('experience').values_list('experience', flat=True))

    if experiences:
        main_exp = experiences[0]
        extra_exp = experiences[1:5]
    else:
        main_exp = None
        extra_exp = []

    last_exp = Experience.get_last_experiences()
    visited_exp = Experience.get_visited_experiences()
    rated_exp = Experience.get_rated_experiences()

    packages = BackupPackage.objects.filter(
        id__in=HomePackage.objects.all().select_related('package').values_list('package', flat=True))
    if packages:
        main_pack = packages[0]
        extra_pack = packages[1:5]
        left_pack = packages[6:8]
    else:
        main_pack = None
        extra_pack = []
        left_pack = []

    services = Experience.SERVICES

    uni_list = University.objects.filter(confirm=True)

    view_users_perm = PermissionController.has_permission(request.user, PermissionController.USER_PERM)
    upgrade_perm = PermissionController.has_permission(request.user, PermissionController.UPGRADE_PERM)
    manage_exp = PermissionController.has_permission(request.user, PermissionController.EXP_MANAGER_PERM)
    manage_upgrade_perm = PermissionController.has_permission(request.user, PermissionController.UPGRADE_MANAGER_PERM)

    return render(request, 'home/home.html',
                  locals())
