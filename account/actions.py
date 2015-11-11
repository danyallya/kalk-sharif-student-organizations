from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import render

from account.forms import CheckUpgradeForm
from account.models import UpgradeMemberRequest, OrganizationMember, Account, Notification
from utils.manager.action import ManagerAction

__author__ = 'M.Y'


class CheckRequestAction(ManagerAction):
    is_view = True
    action_name = 'edit'
    action_verbose_name = u"بررسی"
    form_title = u"بررسی درخواست ارتقا"

    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        obj = selected_instances[0]

        if http_request.method == 'POST':
            form = CheckUpgradeForm(http_request.POST, http_request.FILES, instance=obj, http_request=http_request)

            if form.is_valid():
                obj = form.save()
                form = None
                if http_request.POST.get('accept-submit'):
                    OrganizationMember.create_from_request(obj)

                    user = obj.user
                    if obj.is_organizer:
                        user.level = Account.ORGANIZER_LEVEL
                    else:
                        user.level = Account.ACTIVE_LEVEL
                    user.first_name = obj.first_name
                    user.last_name = obj.last_name
                    user.gender = obj.gender
                    user.mobile = obj.mobile
                    user.save()

                    obj.state = UpgradeMemberRequest.STATE_ACCEPTED
                    obj.save()

                    Notification.send_notify(obj.user, "تایید درخواست ارتقا",
                                             "سطح کاربری شما به '%s' ارتقا یافت" % user.get_level_display())

                    messages.success(http_request, "درخواست مورد نظر تایید شد.")
                elif http_request.POST.get('reject-submit'):
                    obj.state = UpgradeMemberRequest.STATE_REJECT
                    obj.save()

                    Notification.send_notify(obj.user, "رد درخواست ارتقا",
                                             "درخواست شما برای ارتقا سطح کاربری رد شد.")

                    messages.success(http_request, "درخواست مورد نظر رد شد.")
        else:
            form = CheckUpgradeForm(instance=obj, http_request=http_request)

        return render(http_request, 'account/check_request.html',
                      {'form': form, 'title': self.form_title, 'obj': obj})
