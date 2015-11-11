import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from account.permissions import PermissionController, permission_required
from comment.models import UserRate
from document.forms import DocumentForm, DocumentLevelForm, DocumentFirstLevel, DocumentSecondLevel, DocumentThirdLevel, \
    BackupPackageForm
from document.models import Document, DocumentLevel, DocumentContentType, DocumentLevelContentType, BackupPackage, \
    BackupPackageContentType, PackageSubCat
from document.templatetags.doc_template_tags import render_levels_content
from document.util import sorted_by_count, LevelHandler, get_package_cats
from experience.models import Experience


@login_required
def add_document(request):
    if not request.GET.get('in'):
        base_html = 'manager/actions/add_edit_with_base.html'
    else:
        base_html = 'manager/actions/add_edit.html'

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, http_request=request)
        if form.is_valid():
            obj = form.save()
            messages.success(request, u"%s با موفقیت انجام شد." % "افزودن سند")
            return HttpResponseRedirect(reverse('edit_document', args=[obj.id]))
    else:
        form = DocumentForm(http_request=request)

    return render(request, 'document/add.html',
                  {'form': form, 'title': "افزودن سند", 'base_html': base_html})


@login_required
def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    levels = DocumentLevel.objects.filter(document=document).order_by('id')
    return render(request, 'document/edit_page.html',
                  {'levels': levels, 'document': document, 'content_type_id': DocumentContentType.id,
                   'level_content_type_id': DocumentLevelContentType.id})


@login_required
def add_level(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    res = ""
    success = False

    level_id = request.POST.get('id')
    title = request.POST.get('text')

    if title:
        if level_id:
            parent_level = get_object_or_404(DocumentLevel, id=level_id)
            depth = parent_level.depth + 1
        else:
            depth = 1

        level = DocumentLevel(document=document, parent_id=level_id, title=title,
                              depth=depth)
        level.save()

        res = LevelHandler(levels=[], edit=True).render_new_level(level)
        success = True

    return HttpResponse(json.dumps({'s': success, 'res': res}), 'application/json')


@login_required
def delete_level(request):
    success = False

    if request.method == 'POST':
        level_id = request.POST.get('id')
        level = get_object_or_404(DocumentLevel, id=level_id)
        level.delete()
        success = True

    return HttpResponse(json.dumps({'s': success}), 'application/json')


@login_required
def edit_level(request, level_id):
    obj = get_object_or_404(DocumentLevel, id=level_id)

    if not request.GET.get('in'):
        base_html = 'manager/actions/add_edit_with_base.html'
    else:
        base_html = 'manager/actions/add_edit.html'

    if obj.depth == 1:
        form_class = DocumentFirstLevel
    elif obj.depth == 2:
        form_class = DocumentSecondLevel
    elif obj.depth == 3:
        form_class = DocumentThirdLevel
    else:
        form_class = DocumentLevelForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj, http_request=request)

        if form.is_valid():
            obj = form.save()
            messages.success(request, u"%s با موفقیت انجام شد." % "ویرایش طبقه")

        new_level_title = request.POST.get('level-name')
        if new_level_title:
            DocumentLevel.objects.create(document_id=obj.document_id, parent_id=level_id, title=new_level_title,
                                         depth=obj.depth + 1)
            messages.success(request, u"%s با موفقیت انجام شد." % "افزودن طبقه")

    else:
        form = form_class(instance=obj, http_request=request)

    levels = DocumentLevel.objects.filter(parent_id=level_id)

    return render(request, 'document/edit.html',
                  {'form': form, 'title': "ویرایش", 'level_obj': obj, 'levels': levels,
                   'base_html': base_html})


@permission_required(perm=PermissionController.DOC_PERM)
def documents_list(request):
    documents = Document.objects.filter().order_by('-id')

    visited_docs = documents.order_by('-visitor_count')[:4]
    spec_docs = documents.filter(spec__isnull=False)[:4]
    rated_docs = documents.order_by('-rate')[:4]
    commented_docs = documents.order_by('-comment_count')[:4]

    service = request.GET.get('s')
    if service:
        documents = documents.filter(service=service)

    documents = documents.order_by('order')[:12]

    services = Experience.SERVICES

    return render(request, 'document/list.html',
                  {'documents': documents, 'services': services, 'visited_docs': visited_docs,
                   'spec_docs': spec_docs, 'rated_docs': rated_docs, 'commented_docs': commented_docs,
                   'active_service': service})


@permission_required(perm=PermissionController.PACKAGE_PERM)
def package_list(request):
    packages = BackupPackage.objects.filter(confirm=True).order_by('-id')
    cat_items = get_package_cats()

    cat = request.GET.get('c')
    if cat:
        packages = packages.filter(cat_id=cat)

    cat_parent = request.GET.get('ca')
    if cat_parent:
        cat_parent = int(cat_parent)
        packages = packages.filter(cat__cat=cat_parent)
    elif cat:
        cat_parent = get_object_or_404(PackageSubCat, id=cat).cat

    q = request.GET.get('q')
    if q:
        packages = packages.filter(Q(title__icontains=q) | Q(tags__title__icontains=q))

    order_by = request.GET.get('o')
    if order_by == '1':
        order_by = "جدیدترین ها"

    elif str(order_by) == '2':
        packages = packages.order_by('-visitor_count')
        order_by = "پربازدیدترین ها"

    elif str(order_by) == '3':
        packages = packages.order_by('-rate')
        order_by = "پرامتیازترین ها"

    packages = packages[:12]

    return render(request, 'document/packages.html',
                  {'packages': packages, 'cat_items': cat_items, 'order_by': order_by, 'q': q,
                   'cat_parent': cat_parent})


@permission_required(perm=PermissionController.PACKAGE_PERM)
def package_list_load(request):
    packages = BackupPackage.objects.filter(confirm=True).order_by('-id')

    cat = request.GET.get('c')
    if cat:
        packages = packages.filter(cat_id=cat)

    cat_parent = request.GET.get('ca')
    if cat_parent:
        cat_parent = int(cat_parent)
        packages = packages.filter(cat__cat=cat_parent)

    q = request.GET.get('q')
    if q:
        packages = packages.filter(Q(title__icontains=q) | Q(tags__title__icontains=q))

    order_by = request.GET.get('o')
    if str(order_by) == '2':
        packages = packages.order_by('-visitor_count')
    elif str(order_by) == '3':
        packages = packages.order_by('-rate')

    last_index = int(request.GET.get('last_index'))

    packages = packages[last_index + 1:last_index + 9:]

    res = ""

    for idx, package in enumerate(packages):
        res += render_to_string('document/packages_list_item.html', {'obj': package})

    return HttpResponse(mark_safe(res))


@login_required
def send_package(request):
    if request.method == 'POST':
        form = BackupPackageForm(request.POST, request.FILES, http_request=request)
        if form.is_valid():
            obj = form.save()
            messages.success(request, u"افزودن بسته پشتیبان با موفقیت انجام شد.")
            return HttpResponseRedirect(reverse('package_list'))
    else:
        form = BackupPackageForm(http_request=request)
    return render(request, 'manager/actions/add_edit_with_base.html',
                  {'form': form, 'title': "افزودن بسته پشتیبان"})


def document_page(request, document_id):
    try:
        document = PermissionController.get_queryset(request.user, PermissionController.DOC_PERM).get(id=document_id)
    except Document.DoesNotExist:
        return HttpResponseForbidden()

    document.add_visit()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    try:
        rate_obj = UserRate.objects.filter(
            content_type=DocumentContentType,
            object_pk=document_id,
        )
        if request.user.is_anonymous():
            rate_obj = rate_obj.get(ip_address=ipaddress)
        else:
            rate_obj = rate_obj.get(
                Q(user=request.user if not request.user.is_anonymous() else None) | Q(ip_address=ipaddress))
        rate = rate_obj.rate
    except UserRate.DoesNotExist:
        rate = 0

    levels = DocumentLevel.objects.filter(document=document).order_by('id')

    references = sorted_by_count(Experience.objects.filter(document_levels__document=document))

    return render(request, 'document/page.html',
                  {'document': document, 'rate': str(rate), 'levels': levels,
                   'references': references, 'content_type_id': DocumentContentType.id,
                   'level_content_type_id': DocumentLevelContentType.id})


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
                content_type=DocumentContentType,
                object_pk=obj_id,
            )
            if request.user.is_anonymous():
                rate_obj = rate_obj.get(ip_address=ipaddress)
            else:
                rate_obj = rate_obj.get(
                    Q(user=request.user if not request.user.is_anonymous() else None) | Q(ip_address=ipaddress))
        except UserRate.DoesNotExist:
            rate_obj = UserRate(
                content_type=DocumentContentType,
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


def doc_references(request):
    level_id = request.GET.get('id')
    level = get_object_or_404(DocumentLevel, id=level_id)
    references = level.references.all()
    return render(request, 'document/references.html', {'references': references})


def doc_content(request, document_id):
    try:
        document = PermissionController.get_queryset(request.user, PermissionController.DOC_PERM).get(id=document_id)
    except Document.DoesNotExist:
        return HttpResponseForbidden()
    levels = DocumentLevel.objects.filter(document=document).order_by('id')
    return HttpResponse(mark_safe(render_levels_content(levels=levels)))


def package_page(request, package_id):
    try:
        package = PermissionController.get_queryset(request.user, PermissionController.PACKAGE_PERM).get(id=package_id)
    except BackupPackage.DoesNotExist:
        return HttpResponseForbidden()

    package.add_visit()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    try:
        rate_obj = UserRate.objects.filter(
            content_type=BackupPackageContentType,
            object_pk=package_id,
        )
        if request.user.is_anonymous():
            rate_obj = rate_obj.get(ip_address=ipaddress)
        else:
            rate_obj = rate_obj.get(
                Q(user=request.user if not request.user.is_anonymous() else None) | Q(ip_address=ipaddress))
        rate = rate_obj.rate
    except UserRate.DoesNotExist:
        rate = 0

    tags = package.tags.all()

    related_packages = BackupPackage.objects.filter(tags__in=tags).exclude(id=package_id) \
        .annotate(tag_matches=models.Count('tags')).order_by('-tag_matches')

    return render(request, 'document/package_page.html',
                  {'package': package, 'related_packages': related_packages, 'rate': str(rate),
                   'content_type_id': BackupPackageContentType.id, })


def package_send_rate(request):
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
                content_type=BackupPackageContentType,
                object_pk=obj_id,
            )
            if request.user.is_anonymous():
                rate_obj = rate_obj.get(ip_address=ipaddress)
            else:
                rate_obj = rate_obj.get(
                    Q(user=request.user if not request.user.is_anonymous() else None) | Q(ip_address=ipaddress))
        except UserRate.DoesNotExist:
            rate_obj = UserRate(
                content_type=BackupPackageContentType,
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


def package_download(request, package_id):
    try:
        package = PermissionController.get_queryset(request.user, PermissionController.PACKAGE_PERM).get(id=package_id)
    except BackupPackage.DoesNotExist:
        return HttpResponseForbidden()

    package.receive_count += 1
    package.save()
    return HttpResponseRedirect(package.pdf_file.url)
