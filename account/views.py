import json
import string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from django.views.decorators.cache import never_cache

from account.forms import SignUpForm, AccountForm, UpgradeMemberForm, ActiveAccountForm, ChangeMemberForm
from account.models import UpgradeMemberRequest, Notification, Account
from account.permissions import PermissionController
from document.models import BackupPackage, Document
from experience.models import Experience
from utils.messages import MessageServices


@never_cache
def logout(request):
    from django.contrib.auth import logout

    next_page = request.GET.get('next', '/')

    logout(request)
    return HttpResponseRedirect(next_page)


def login(request):
    from django.contrib.auth import authenticate, login

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            messages.error(request, u"نام کاربری یا گذرواژه نادرست است.")
        else:
            login(request, user)
            next_page = request.GET.get('next', '/')
            if next_page:
                return HttpResponseRedirect(next_page)

    context = {
        'app_path': request.get_full_path(),
        'next': request.get_full_path(),
    }

    return render(request, 'account/login.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST.copy())
        if form.is_valid():
            profile = form.save()
            messages.success(request, u"ثبت نام شما با موفقیت انجام شد. اکنون می توانید وارد شوید.")
            next_page = request.GET.get('next', '/')

            return HttpResponseRedirect(reverse('login') + "?next=" + next_page)
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


@login_required
def account_page(request):
    view_users_perm = PermissionController.has_permission(request.user, PermissionController.USER_PERM)
    upgrade_perm = PermissionController.has_permission(request.user, PermissionController.UPGRADE_PERM)
    manage_exp = PermissionController.has_permission(request.user, PermissionController.EXP_MANAGER_PERM)
    manage_upgrade_perm = PermissionController.has_permission(request.user, PermissionController.UPGRADE_MANAGER_PERM)

    is_admin = PermissionController.is_admin(request.user)

    # return render(request, 'account/page_new.html',{})

    return render(request, 'account/page.html',
                  {'view_users_perm': view_users_perm, 'upgrade_perm': upgrade_perm, 'manage_exp': manage_exp,
                   'manage_upgrade_perm': manage_upgrade_perm, 'is_admin': is_admin})


@login_required
def edit_account(request):
    request_instance = None
    organize_form = None

    is_active_user = PermissionController.is_active_user(request.user)

    EditForm = AccountForm
    if is_active_user:
        EditForm = ActiveAccountForm
        request_instance = UpgradeMemberRequest.get_for_user(request.user)

    edit_form = EditForm(instance=request.user, http_request=request, prefix='edit')
    if is_active_user:
        organize_form = ChangeMemberForm(instance=request_instance, http_request=request, prefix='organize')

    if request.method == 'POST':
        if request.POST.get('edit-submit'):
            edit_form = EditForm(request.POST.copy(), instance=request.user, http_request=request, prefix='edit')
            request_form = ChangeMemberForm(request.POST.copy(), instance=request_instance, http_request=request)
            if edit_form.is_valid():
                profile = edit_form.save()
                messages.success(request, "ویرایش حساب کاربری با موفقیت انجام شد.")

                return HttpResponseRedirect(reverse('account_page'))
        else:
            if is_active_user:
                organize_form = ChangeMemberForm(request.POST.copy(), instance=request_instance, http_request=request,
                                                 prefix='organize')
                if organize_form.is_valid():
                    obj = organize_form.save()
                    member_obj = request.user.get_current_organization_member()
                    if member_obj:
                        member_obj.update(obj)
                    messages.success(request, "ویرایش حساب کاربری با موفقیت انجام شد.")
                    return HttpResponseRedirect(reverse('account_page'))

    return render(request, 'account/edit.html', {'edit_form': edit_form, 'organize_form': organize_form})


@login_required
def upgrade(request):
    try:
        instance = UpgradeMemberRequest.objects.get(user=request.user)
        message = "درخواست شما قبلا ثبت شده است. از این قسمت می توانید درخواست را ویرایش نمایید. وضعیت درخواست: " + instance.form_state
    except UpgradeMemberRequest.DoesNotExist:
        instance = None
        message = ""

    if request.method == 'POST':
        form = UpgradeMemberForm(request.POST.copy(), instance=instance, http_request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "درخواست ارتقا سطح کاربری با موفقیت ثبت شد.")
            Notification.send_to_organizer(request.user, "درخواست ارتقا جدید",
                                           "یک درخواست ارتقای سطح کاربری جدید ارسال شده است.")
            return HttpResponseRedirect(reverse('account_page'))
    else:
        form = UpgradeMemberForm(instance=instance, http_request=request)
    return render(request, 'manager/actions/add_edit_with_base.html',
                  {'form': form, 'title': "درخواست ارتقا سطح کاربری", 'message': message})


@login_required
def seen_notification(request, notification_id):
    get_object_or_404(Notification, id=notification_id).set_seen()
    return HttpResponseRedirect(reverse('account_page'))


def search(request):
    q = request.GET.get('q')

    experiences = Experience.objects.filter(confirm=True).order_by('-id').filter(
        Q(tags__title__icontains=q) | Q(title__icontains=q))

    packages = BackupPackage.objects.filter(confirm=True).order_by('-id').filter(
        Q(tags__title__icontains=q) | Q(title__icontains=q))

    documents = Document.objects.filter().order_by('-id').filter(Q(tags__title__icontains=q) | Q(title__icontains=q))

    return render(request, 'account/search.html', locals())


def forget(request):
    message = ""
    success = False
    if request.method == 'POST':
        email = request.POST.get('email')
        if email and Account.objects.filter(email=email).exists():
            MessageServices.send_forget_password(email)
            message = u"رمز عبور به ایمیل شما ارسال خواهد شد."
            success = True
        else:
            message = "این ایمیل پیدا نشد."
            success = False

    res = {'s': success, 'm': message}
    return HttpResponse(json.dumps(res), 'application/json')


def change_pass(request):
    code = request.GET.get('c')
    if not code:
        raise Http404
    user = get_object_or_404(Account, code=code)
    new_pass = Account.objects.make_random_password(10, string.ascii_lowercase)
    user.set_password(new_pass)
    user.save()
    return render(request, 'account/change_pass.html', {'user': user, 'new_pass': new_pass})
