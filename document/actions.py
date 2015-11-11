from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from document.forms import DocumentForm, BackupPackageFormset
from document.models import DocumentLevel

from utils.manager.action import ManagerAction

__author__ = 'M.Y'


class AddDocument(ManagerAction):
    is_view = True
    action_name = 'add'
    action_verbose_name = u"افزودن"
    form_title = u"افزودن"

    def action_view(self, http_request, selected_instances):
        return HttpResponseRedirect(reverse('add_document') + "?in=1")


class EditDocument(ManagerAction):
    is_view = True
    action_name = 'edit'
    action_verbose_name = u"ویرایش"
    form_title = u"ویرایش"

    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        obj = selected_instances[0]

        if http_request.method == 'POST':
            form = DocumentForm(http_request.POST, http_request.FILES, instance=obj, http_request=http_request)

            if form.is_valid():
                obj = form.save()
                form = DocumentForm(instance=obj, http_request=http_request)
                messages.success(http_request, u"%s با موفقیت انجام شد." % "ویرایش سند")

            new_level_title = http_request.POST.get('level-name')
            if new_level_title:
                DocumentLevel.objects.create(document=obj, title=new_level_title)
                messages.success(http_request, u"%s با موفقیت انجام شد." % "افزودن طبقه")

        else:
            form = DocumentForm(instance=obj, http_request=http_request)

        # levels = DocumentLevel.objects.filter(document=obj, depth=1)

        return render(http_request, 'document/edit.html',
                      {'form': form, 'title': "ویرایش", 'doc': obj})


class EditLevelsAction(ManagerAction):
    is_view = True
    new_tab = True
    action_name = 'edit_levels'
    action_verbose_name = u"ویرایش طبقات"
    form_title = u"ویرایش طبقات"

    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        obj = selected_instances[0]
        return HttpResponseRedirect(reverse('edit_document', args=[obj.id]))


class BackupPackageEdit(ManagerAction):
    is_view = True
    action_name = 'backup_edit'
    action_verbose_name = u"بسته های پشتیبان مربوطه"
    form_title = u"بسته های پشتیبان مربوطه"

    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        obj = selected_instances[0]

        if http_request.method == 'POST':
            formset = BackupPackageFormset(http_request.POST, http_request.FILES, prefix='backup',
                                           instance=obj)
            if formset.is_valid():
                ins = formset.save(commit=False)
                for o in ins:
                    o.gallery = obj
                    o.save()
                formset = None
                messages.success(http_request, u"ویرایش بسته های پشتیبان با موفقیت انجام شد.")

        else:
            formset = BackupPackageFormset(prefix='backup', instance=obj)

        return render(http_request, 'document/backup_form.html',
                      {'title': self.form_title, 'formset': formset})
