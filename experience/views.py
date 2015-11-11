import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from account.models import Notification

from account.permissions import PermissionController, permission_required
from comment.models import UserRate
from experience.forms import ExperienceForm, ImageFormset, AttachmentFormset, SendImageForm
from experience.models import Experience, ExperienceContentType, Place, University
from utils.calverter import jalali_to_gregorian
from utils.models import Gallery


@permission_required(perm=PermissionController.EXP_PERM)
def experiences_list(request):
    tag_id = request.GET.get('t')
    experiences = Experience.objects.filter(confirm=True).order_by('-id')
    if tag_id:
        experiences = experiences.filter(tags__id=tag_id).distinct()
    services = Experience.SERVICES

    s = request.GET.get('s')
    y = request.GET.get('y')
    t = request.GET.get('t')
    tn = request.GET.get('tn')
    uni = request.GET.get('uni')
    if s:
        experiences = experiences.filter(service=s)
    if y and y.isdigit():
        from_date = jalali_to_gregorian("%s/01/01" % y)
        until_date = jalali_to_gregorian("%s/01/01" % (int(y) + 1))
        experiences = experiences.filter(date__gte=from_date, date__lt=until_date)
    if t:
        experiences = experiences.filter(tags__id=t)

    uni_list = []
    if uni:
        uni = get_object_or_404(University, id=uni)
        experiences = experiences.filter(university=uni)
        uni_list = University.objects.filter(uni_type=uni.uni_type, state_id=uni.state_id)

    experiences = experiences[:11]

    states = Place.objects.all()

    return render(request, 'experience/list.html',
                  {'experiences': experiences, 'services': services, 's': s, 'y': y, 't': t, 'tn': tn,
                   'uni': uni, 'uni_list': uni_list, 'states': states})


@permission_required(perm=PermissionController.EXP_PERM)
def experiences_list_load(request):
    tag_id = request.GET.get('t')
    experiences = Experience.objects.filter(confirm=True).order_by('-id')
    if tag_id:
        experiences = experiences.filter(tags__id=tag_id).distinct()
    services = Experience.SERVICES

    s = request.GET.get('s')
    y = request.GET.get('y')
    t = request.GET.get('t')
    tn = request.GET.get('tn')
    uni = request.GET.get('uni')
    if s:
        experiences = experiences.filter(service=s)
    if y and y.isdigit():
        from_date = jalali_to_gregorian("%s/01/01" % y)
        until_date = jalali_to_gregorian("%s/01/01" % (int(y) + 1))
        experiences = experiences.filter(date__gte=from_date, date__lt=until_date)
    if t:
        experiences = experiences.filter(tags__id=t)

    if uni:
        uni = get_object_or_404(University, id=uni)
        experiences = experiences.filter(university=uni)

    last_index = int(request.GET.get('last_index'))

    experiences = experiences[last_index + 1:last_index + 7:]

    res = ""

    for idx, experience in enumerate(experiences):
        res += render_to_string('experience/list_item.html', {'obj': experience, 'order': 12 - idx})

    return HttpResponse(mark_safe(res))


def experience_page(request, experience_id):
    try:
        experience = PermissionController.get_queryset(request.user, PermissionController.EXP_PERM).get(
            id=experience_id)
    except Experience.DoesNotExist:
        return HttpResponseForbidden()

    experience.add_visit()

    tags = experience.tags.all()

    related_ex = Experience.objects.filter(tags__in=tags).exclude(id=experience_id) \
        .annotate(tag_matches=models.Count('tags')).order_by('-tag_matches')

    experience.prepare_attachments()

    experience_images = experience.gallery.images.filter(confirm=True) if experience.gallery_id else []

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    try:
        rate_obj = UserRate.objects.filter(
            content_type=ExperienceContentType,
            object_pk=experience_id,
        )
        if request.user.is_anonymous():
            rate_obj = rate_obj.get(ip_address=ipaddress)
        else:
            rate_obj = rate_obj.get(
                Q(user=request.user if not request.user.is_anonymous() else None) | Q(ip_address=ipaddress))
        rate = rate_obj.rate
    except UserRate.DoesNotExist:
        rate = 0

    return render(request, 'experience/page.html',
                  {'experience': experience, 'related_ex': related_ex,
                   'experience_images': experience_images, 'rate': str(rate),
                   'content_type_id': ExperienceContentType.id})


def send_image(request):
    if request.method == 'POST':
        form = SendImageForm(request.POST, request.FILES)

        try:
            experience = PermissionController.get_queryset(request.user, PermissionController.EXP_PERM).get(
                id=request.POST.get('experience_id'))
        except Experience.DoesNotExist:
            return HttpResponseForbidden()

        if form.is_valid():
            if not experience.gallery_id:
                gallery = Gallery.objects.create()
                experience.gallery = gallery
                experience.save()

            image_obj = form.save(commit=False)
            image_obj.gallery_id = experience.gallery_id

            if not request.user.is_anonymous():
                image_obj.confirm = True
            else:
                image_obj.confirm = False
                Notification.send_to_organizer(request.user, "عکس جدید", "یک عکس جدید تاییدنشده فرستاده شده است.")

            image_obj.save()
            messages.success(request, "تصویر با موفقیت ذخیره شد.")
        else:
            messages.error(request, form.errors['image'])
        return HttpResponseRedirect(reverse(experience_page, args=[experience.id]))
    raise Http404


@login_required
def add_experience(request):
    image_formset = ImageFormset(prefix='image')
    attach_formset = AttachmentFormset(prefix='attach')
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES, http_request=request)
        if form.is_valid():
            obj = form.save()
            form = None
            if not obj.gallery:
                gallery = Gallery.objects.create()
                obj.gallery = gallery
                obj.save()
            image_formset = ImageFormset(request.POST, request.FILES, prefix='image', instance=obj.gallery)
            if image_formset.is_valid():
                images = image_formset.save(commit=False)
                for image in images:
                    image.gallery = obj.gallery
                    image.save()
            attach_formset = AttachmentFormset(request.POST, request.FILES, prefix='attach', instance=obj)
            if attach_formset.is_valid():
                attach = attach_formset.save(commit=True)
            if obj.confirm:
                messages.success(request, u"افزودن تجربه با موفقیت انجام شد.")
            else:
                messages.success(request, "تجربه شما ثبت شد و پس از تایید نمایش داده خواهد شد")
            return HttpResponseRedirect(reverse('experiences_list'))
    else:
        form = ExperienceForm(http_request=request)

    return render(request, 'experience/experience_form.html',
                  {'form': form, 'title': "افزودن تجربه", 'image_formset': image_formset,
                   'attach_formset': attach_formset})


def send_rate(request):
    obj_id = request.POST.get('id')
    rate = request.POST.get('rate')
    res = False

    try:
        if int(rate) > 5:
            raise Http404
    except (ValueError, TypeError):
        raise Http404

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    if rate:
        try:
            rate_obj = UserRate.objects.filter(
                content_type=ExperienceContentType,
                object_pk=obj_id,
            )
            if request.user.is_anonymous():
                rate_obj = rate_obj.get(ip_address=ipaddress)
            else:
                rate_obj = rate_obj.get(
                    Q(user=request.user if not request.user.is_anonymous() else None) | Q(ip_address=ipaddress))
        except UserRate.DoesNotExist:
            rate_obj = UserRate(
                content_type=ExperienceContentType,
                object_pk=obj_id,
                ip_address=ipaddress
            )
        rate_obj.user = request.user if not request.user.is_anonymous() else None
        rate_obj.rate = rate
        rate_obj.save()
        res = True
        message = "امتیاز شما با موفقیت ثبت شد"
    else:
        message = "اشکال در ارسال داده ها"
    return HttpResponse(json.dumps({'res': res, 'message': message}), 'application/json')
