from django.contrib import messages
from django.http.response import Http404

from django.shortcuts import render

from experience.forms import ImageFormset
from utils.forms import create_model_form
from utils.manager.action import DeleteAction, ManagerAction, EditAction, AddAction, DoAction
from utils.manager.main import ObjectsManager, ManagerColumn
from utils.models import Gallery, HelpCase, ImageModel

__author__ = 'M.Y'


class EditGallery(ManagerAction):
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
            image_formset = ImageFormset(http_request.POST, http_request.FILES, prefix='image',
                                         instance=obj)
            if image_formset.is_valid():
                images = image_formset.save(commit=False)
                for image in images:
                    image.gallery = obj
                    image.save()
                image_formset = None
                messages.success(http_request, u"%s با موفقیت انجام شد." % self.form_title)

        else:
            image_formset = ImageFormset(prefix='image', instance=obj)

        return render(http_request, 'utils/gallery_form.html',
                      {'title': self.form_title, 'image_formset': image_formset})


def confirm_obj(http_request, selected_instances):
    for p in selected_instances:
        p.confirm = True
        p.save()


class GalleryManager(ObjectsManager):
    manager_name = u"gallery_manager"
    manager_verbose_name = "عکس ها"
    actions = [
        EditAction(create_model_form(ImageModel)),
        DeleteAction(),
        DoAction(do_function=confirm_obj, action_name='confirm', action_verbose_name="تایید",
                 confirm_message="آیا از تایید موارد انتخاب شده اطمینان دارید؟")
    ]

    def get_all_data(self):
        return ImageModel.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('id', u"شماره", 1),
            ManagerColumn('image', u"عکس", 9),
            ManagerColumn('confirm', u"تاییدشده", 3),
        ]
        return columns


HelpCaseForm = create_model_form(HelpCase)


class HelpManager(ObjectsManager):
    manager_name = u"help_manager"
    manager_verbose_name = "راهنما ها"
    actions = [
        AddAction(HelpCaseForm),
        EditAction(HelpCaseForm),
        DeleteAction(),
    ]

    def get_all_data(self):
        return HelpCase.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('code', u"عنصر", 3),
            ManagerColumn('text', u"متن", 7),
        ]
        return columns
