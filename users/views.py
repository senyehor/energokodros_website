from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as LogView
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from administrator.logic import is_admin
from users.forms import (
    LoginForm,
    NewUserForm,
    UserRoleApplicationForm,
)
from users.logic import remember_user_for_two_week, UserRegistrationController


class LoginView(LogView):
    authentication_form = LoginForm

    def form_valid(self, form):
        if form.data.get('remember_me'):
            remember_user_for_two_week(self.request)
        return super().form_valid(form)


class CreateUserRegistrationRequest(CreateView):
    form_class = NewUserForm
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['role_application_form'] = UserRoleApplicationForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        user_form = self.form_class(self.request.POST or None)
        role_application_without_user = UserRoleApplicationForm(
            data=self.request.POST or None
        )
        if user_form.is_valid() and role_application_without_user.is_valid():
            return self.form_valid(user_form, role_application_without_user)
        return self.form_invalid(user_form, role_application_without_user)

    @method_decorator(transaction.atomic)
    def form_valid(self, user_form: NewUserForm,  # noqa pylint: disable=W0221
                   role_application_without_user_form: UserRoleApplicationForm):
        controller = UserRegistrationController(user_form, role_application_without_user_form)
        self.object = controller.save_user_along_with_registration_request_return_user()
        if controller.send_email_confirmation_message(self.request):
            return redirect(reverse('successfully-created-registration-request'))
        transaction.rollback()
        return HttpResponse(status=500)

    def form_invalid(  # noqa pylint: disable=W0221
            self, user_form: NewUserForm,
            role_application_formset:
            UserRoleApplicationForm):
        return self.render_to_response(
            self.get_context_data(
                user_form=user_form,
                role_application_formset=
                role_application_formset,
            ),
            status=400
        )


@login_required
def index_view(request: HttpRequest):
    if is_admin(request):
        return redirect(reverse('admin-page'))
    return render(request, 'index.html')


def successfully_created_registration_request(request):
    return render(request, 'registration/successfully_created_registration_request.html')


def confirm_email(request: HttpRequest, user_id: int, user_email: str):
    UserRegistrationController.confirm_email_if_user_exists(user_id, user_email)
    return redirect('successfully-confirmed-email')


def successfully_confirmed_email(request: HttpRequest):
    return render(request, 'registration/successfully_confirmed_email.html')


class ProfilesView(View):
    """currently it is just a stub"""

    def get(self, request):
        return render(request, 'index.html')
