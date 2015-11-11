import copy
from django.core import validators
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.utils.encoding import force_text
from django_select2.fields import AutoModelSelect2TagField, AutoModelSelect2Field
from django_select2.views import NO_ERR_RESP
from django_select2.widgets import AutoHeavySelect2Widget
from account.models import Organization, Role
from experience.models import University, Tag
from utils.models import Certifiable

__author__ = 'M.Y'


# class TitledMultipleModelField(AutoModelSelect2TagField):
#     search_fields = ['title__icontains']
#     queryset = None  # IS REQUIRED
#
#     def get_model_field_values(self, value):
#         return {'title': value}


class TitledModelWidget(AutoHeavySelect2Widget):
    def init_options(self):
        self.options['createSearchChoice'] = '*START*createIfNotExist*END*'

    def render_texts_for_value(self, id_, value, choices):
        empty_values = getattr(self.field, 'empty_values', validators.EMPTY_VALUES)
        if value is not None and (self.field is None or value not in empty_values):
            try:
                value = int(value)
                values = [value]
                texts = self.render_texts(values, choices)
                if texts:
                    return "$('#%s').txt(%s);" % (id_, texts)
            except:
                pass


class TitledModelField(AutoModelSelect2Field):
    search_fields = ['title__icontains']
    widget = TitledModelWidget
    empty_values = list(validators.EMPTY_VALUES)
    default_error_messages = {
        'invalid_choice': "مقدار انتخاب شده معتبر نمی باشد",
    }

    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(TitledModelField, self).__init__(*args, **kwargs)

    def get_model_field_values(self, value):
        return {'title': value}

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            value = self.queryset.get(**{key: value})
        except ValueError:
            raise ValidationError(self.error_messages['invalid_choice'])
        except self.queryset.model.DoesNotExist:
            value = self.create_new_value(value)
        return value

    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        elif not self.required and not value:
            return []
        key = self.to_field_name or 'pk'
        try:
            new_value = self.queryset.get(**{key: value})
        except ValueError:
            new_value = self.create_new_value(force_text(value))

        # qs = self.queryset.filter(**{'%s__in' % key: value})
        # pks = set([force_text(getattr(o, key)) for o in qs])
        # for i in range(0, len(value)):
        #     val = force_text(value[i])
        #     if val not in pks:
        #         value[i] = self.create_new_value(val)
        self.run_validators(new_value)
        return new_value

    def create_new_value(self, value):
        arg = {"title": value}
        if self.http_request.user.is_authenticated():
            arg['creator'] = self.http_request.user
        obj = self.queryset.create(**arg)
        return obj

    def get_results(self, request, term, page, context):
        """
        See :py:meth:`.views.Select2View.get_results`.

        This implementation takes care of detecting if more results are available.
        """
        if not hasattr(self, 'search_fields') or not self.search_fields:
            raise ValueError('search_fields is required.')

        qs = copy.deepcopy(self.get_queryset())

        if issubclass(qs.model, Certifiable):
            qs = qs.filter(Q(confirm=True) | Q(creator=request.user))

        params = self.prepare_qs_params(request, term, self.search_fields)

        if self.max_results:
            min_ = (page - 1) * self.max_results
            max_ = min_ + self.max_results + 1  # fetching one extra row to check if it has more rows.
            res = list(qs.filter(*params['or'], **params['and']).distinct()[min_:max_])
            has_more = len(res) == (max_ - min_)
            if has_more:
                res = res[:-1]
        else:
            res = list(qs.filter(*params['or'], **params['and']).distinct())
            has_more = False

        res = [
            (
                getattr(obj, self.to_field_name),
                self.label_from_instance(obj),
                self.extra_data_from_instance(obj)
            )
            for obj in res
            ]
        return NO_ERR_RESP, has_more, res


class OrganizationChoiceField(TitledModelField):
    queryset = Organization.objects


class UniModelWidget(TitledModelWidget):
    def init_options(self):
        self.options['createSearchChoice'] = '*START*createIfNotExist*END*'
        self.options['ajax'] = {
            'dataType': 'json',
            'quietMillis': 100,
            'data': '*START*django_select2.runInContextHelper(django_select2.s2_state_param_gen, selector)*END*',
            'results': '*START*django_select2.runInContextHelper(django_select2.process_results, selector)*END*',
        }


class UniversityChoiceField(TitledModelField):
    queryset = University.objects
    widget = UniModelWidget

    def get_results(self, request, term, page, context):
        state_id = request.GET.get('state', '')
        uni_type = request.GET.get('uni_type', '')

        if not hasattr(self, 'search_fields') or not self.search_fields:
            raise ValueError('search_fields is required.')

        qs = copy.deepcopy(self.get_queryset())

        if issubclass(qs.model, Certifiable):
            qs = qs.filter(Q(confirm=True) | Q(creator=request.user))

        if state_id:
            qs = qs.filter(state_id=state_id)
        if uni_type:
            qs = qs.filter(uni_type=uni_type)

        params = self.prepare_qs_params(request, term, self.search_fields)

        if self.max_results:
            min_ = (page - 1) * self.max_results
            max_ = min_ + self.max_results + 1  # fetching one extra row to check if it has more rows.
            res = list(qs.filter(*params['or'], **params['and']).distinct()[min_:max_])
            has_more = len(res) == (max_ - min_)
            if has_more:
                res = res[:-1]
        else:
            res = list(qs.filter(*params['or'], **params['and']).distinct())
            has_more = False

        res = [
            (
                getattr(obj, self.to_field_name),
                self.label_from_instance(obj),
                self.extra_data_from_instance(obj)
            )
            for obj in res
            ]
        return NO_ERR_RESP, has_more, res


class RoleChoiceField(TitledModelField):
    queryset = Role.objects


class TagMultipleField(AutoModelSelect2TagField):
    queryset = Tag.objects
    search_fields = ['title__icontains', ]

    def get_model_field_values(self, value):
        return {'title': value}
