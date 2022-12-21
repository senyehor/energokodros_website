from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from users.forms import NewUserForm, UserRoleApplicationFormForRegistration
from users.logic import UserRegistrationController


class CreateUserRegistrationRequestView(CreateView):
    form_class = NewUserForm
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['role_application_form'] = UserRoleApplicationFormForRegistration()
        return ctx

    def post(self, request, *args, **kwargs):
        # noinspection PyAttributeOutsideInit
        self.object = None
        user_form = self.form_class(self.request.POST or None)
        role_application_without_user = UserRoleApplicationFormForRegistration(
            data=self.request.POST or None
        )
        if user_form.is_valid() and role_application_without_user.is_valid():
            return self.form_valid(user_form, role_application_without_user)
        return self.form_invalid(user_form, role_application_without_user)

    @method_decorator(transaction.atomic)
    def form_valid(self, user_form: NewUserForm,  # noqa pylint: disable=W0221
                   role_application_without_user_form: UserRoleApplicationFormForRegistration):
        controller = UserRegistrationController(user_form, role_application_without_user_form)
        # noinspection PyAttributeOutsideInit
        self.object = controller.save_user_along_with_registration_request_return_user()
        if controller.send_email_confirmation_message(self.request):
            return redirect(reverse('successfully-created-registration-request'))
        messages.error(
            self.request,
            _('Не вдалося відправити повідомлення на пошту, перевірте дані та спробуйте ще раз')
        )
        transaction.set_rollback(True)
        return redirect(reverse('register'))

    def form_invalid(  # noqa pylint: disable=W0221
            self, user_form: NewUserForm,
            role_application_form:
            UserRoleApplicationFormForRegistration):
        return self.render_to_response(
            self.get_context_data(
                user_form=user_form,
                role_application_form=
                role_application_form,
            ),
            status=400
        )
