from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import render

from experience.forms import ExperienceForm, ImageFormset, AttachmentFormset
from utils.manager.action import ManagerAction
from utils.models import Gallery

__author__ = 'M.Y'


class AddExperience(ManagerAction):
    is_view = True
    action_name = 'add'
    action_verbose_name = u"افزودن"
    form_title = u"افزودن"

    def action_view(self, http_request, selected_instances):
        image_formset = ImageFormset(prefix='image')
        attach_formset = AttachmentFormset(prefix='attach')
        if http_request.method == 'POST':
            form = ExperienceForm(http_request.POST, http_request.FILES, http_request=http_request)
            if form.is_valid():
                obj = form.save()
                form = None
                if not obj.gallery:
                    gallery = Gallery.objects.create()
                    obj.gallery = gallery
                    obj.save()
                image_formset = ImageFormset(http_request.POST, http_request.FILES, prefix='image',
                                             instance=obj.gallery)
                if image_formset.is_valid():
                    images = image_formset.save(commit=False)
                    for image in images:
                        image.gallery = obj.gallery
                        image.save()
                attach_formset = AttachmentFormset(http_request.POST, http_request.FILES, prefix='attach',
                                                   instance=obj)
                if attach_formset.is_valid():
                    attach = attach_formset.save(commit=True)

                messages.success(http_request, u"%s با موفقیت انجام شد." % self.form_title)
        else:
            form = ExperienceForm(http_request=http_request)

        return render(http_request, 'experience/experience_crud_form.html',
                      {'form': form, 'title': self.form_title, 'image_formset': image_formset,
                       'attach_formset': attach_formset})


class EditExperience(ManagerAction):
    is_view = True
    action_name = 'edit'
    action_verbose_name = u"ویرایش"
    form_title = u"ویرایش"

    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        obj = selected_instances[0]

        if not obj.gallery:
            gallery = Gallery.objects.create()
            obj.gallery = gallery
            obj.save()

        if http_request.method == 'POST':
            image_formset = ImageFormset(http_request.POST, http_request.FILES, prefix='image',
                                         instance=obj.gallery)
            attach_formset = AttachmentFormset(http_request.POST, http_request.FILES, prefix='attach',
                                               instance=obj)
            form = ExperienceForm(http_request.POST, http_request.FILES, instance=obj,
                                  http_request=http_request)
            if form.is_valid():
                obj = form.save()
                form = None
                messages.success(http_request, u"%s با موفقیت انجام شد." % self.form_title)

                if image_formset.is_valid():
                    images = image_formset.save(commit=False)

                    for image in image_formset.deleted_objects:
                        image.delete()

                    for image in images:
                        image.gallery = obj.gallery
                        image.save()

                if attach_formset.is_valid():
                    attach = attach_formset.save(commit=True)
        else:
            form = ExperienceForm(instance=obj, http_request=http_request)
            image_formset = ImageFormset(prefix='image', instance=obj.gallery)
            attach_formset = AttachmentFormset(prefix='attach', instance=obj)

        return render(http_request, 'experience/experience_crud_form.html',
                      {'form': form, 'title': self.form_title, 'image_formset': image_formset,
                       'attach_formset': attach_formset})
