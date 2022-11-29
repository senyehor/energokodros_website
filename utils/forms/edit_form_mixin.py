from typing import Protocol, runtime_checkable, Union

from django.contrib import messages
from django.db.models import Model
from django.forms import Form
from django.views.generic import UpdateView


@runtime_checkable
class NeedsAdditionalFilling(Protocol):
    def additionally_fill(self, operated_object: Model):
        ...


class EditObjectUpdateViewMixin:
    """
    must be used as a mixin for UpdateView, needs to be first in superclass list
    to correctly override methods
    """
    edit_success_message: str = None
    delete_success_message: str = None

    def get_context_data(self, **kwargs):
        # noinspection PyUnresolvedReferences
        data = super().get_context_data(**kwargs)
        self.fill_from_object_if_needed(data)
        return data

    def fill_from_object_if_needed(self: UpdateView, data: dict):
        form: Form = data['form']
        if isinstance(form, NeedsAdditionalFilling):
            form.additionally_fill(self.object)

    def form_valid(self: Union[UpdateView, 'EditObjectUpdateViewMixin'], form):
        messages.success(
            self.request,
            self.edit_success_message
        )
        # noinspection PyUnresolvedReferences
        return super().form_valid(form)
