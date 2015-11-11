from account.permissions import PermissionController

__author__ = 'M.Y'


def default_context(request):
    referrer = ''
    if request.META.get("HTTP_REFERER"):
        referrer = request.META.get("HTTP_REFERER")

    level = 0
    if request.user.is_authenticated():
        level = request.user.level
    context = {'level': level, 'referrer': referrer}
    return context
