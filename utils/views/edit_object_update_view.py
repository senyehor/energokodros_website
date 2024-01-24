from typing import TypeAlias, Union

from django.contrib import messages
from django.db.models import Model
from django.forms import Form
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import UpdateView

from utils.forms.crispy_buttons import DEFAULT_DELETE_VALUE


class AdditionalSetupRequiredFormMixin:
    def additionally_setup(self, obj: Model):
        raise NotImplementedError


_EditDeleteObjectViewWithMixinType: TypeAlias = Union[UpdateView, 'EditDeleteObjectUpdateViewMixin']


class EditDeleteObjectUpdateViewMixin:
    """
    must be used as a mixin for UpdateView, needs to be first in superclass list
    to correctly override methods
    """
    EDIT_SUCCESS_MESSAGE: str = _('Успішно відредаговано')
    DELETE_SUCCESS_MESSAGE: str = _('Успішно видалено')
    NO_CHANGES_MESSAGE: str = _('Ви не внесли жодних змін, тож були перенаправлені')

    def post(self: _EditDeleteObjectViewWithMixinType, request: HttpRequest, *args, **kwargs):
        if request.POST['submit'] == DEFAULT_DELETE_VALUE:
            return self.__delete_object()
        # noinspection PyUnresolvedReferences
        return super().post(request, *args, **kwargs)

    def get_context_data(self: _EditDeleteObjectViewWithMixinType, **kwargs):
        # noinspection PyUnresolvedReferences
        data = super().get_context_data(**kwargs)
        self.fill_from_object_if_needed(data)
        return data

    def fill_from_object_if_needed(self: _EditDeleteObjectViewWithMixinType, data: dict):
        form: Form = data['form']
        if isinstance(form, AdditionalSetupRequiredFormMixin):
            form.additionally_setup(self.object)

    def form_valid(self: _EditDeleteObjectViewWithMixinType, form: Form):
        if form.has_changed():
            messages.success(
                self.request,
                self.EDIT_SUCCESS_MESSAGE
            )
        else:
            messages.info(
                self.request,
                self.NO_CHANGES_MESSAGE
            )
        return super().form_valid(form)

    def __delete_object(self: _EditDeleteObjectViewWithMixinType):
        self.get_object().delete()
        messages.warning(
            self.request,
            self.DELETE_SUCCESS_MESSAGE,
        )
        # default redirect goes to self.get_success_url(), but is uses self.object,
        # which has just been deleted, so redirect to .success_url
        return redirect(self.success_url)


class EditDeleteObjectUpdateView(EditDeleteObjectUpdateViewMixin, UpdateView):
    pass
