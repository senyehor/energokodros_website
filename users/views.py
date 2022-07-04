from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as LogView
from django.db import transaction
from django.forms import BaseInlineFormSet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView

from users.forms import (
    LoginForm,
    NewUserForm,
    RegistrationFormset
)
from users.logic import EmailConfirmationController, remember_user_for_two_week
from users.models import UserRoleApplication


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
        ctx['registration_formset'] = RegistrationFormset()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None  # noqa
        form = self.get_form(self.get_form_class())
        registration_formset = RegistrationFormset(self.request.POST or None)
        if form.is_valid() and registration_formset.is_valid():
            return self.form_valid(form, registration_formset)
        return self.form_invalid(form, registration_formset)

    @method_decorator(transaction.atomic)
    def form_valid(self, form: NewUserForm, registration_formset: RegistrationFormset):  # noqa pylint: disable=W0221
        self.__save_user_with_role_application(form, registration_formset)
        if self.__send_email_confirmation_message():
            return redirect(reverse_lazy('successfully_created_registration_request'))
        # deleting created user and it`s application if we failed to send email confirmation message
        self.__delete_user_with_role_application()
        return HttpResponse(status=500)

    def form_invalid(  # noqa pylint: pylint: disable=W0221
            self, form: NewUserForm,
            registration_formset:
            RegistrationFormset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                registration_formset=
                registration_formset,
            ),
            status=400
        )

    def __delete_user_with_role_application(self):
        self.object.delete()
        self.user_role_application.delete()

    def __save_user_with_role_application(
            self, form: NewUserForm, registration_formset: RegistrationFormset):
        self.object = form.save(commit=False)  # noqa
        self.object.save()
        user_role_application = self.__get_form_from_registration_formset(registration_formset)
        user_role_application.user = self.object
        self.user_role_application = user_role_application
        self.user_role_application.save()

    def __send_email_confirmation_message(self) -> bool:
        return EmailConfirmationController.send_email_confirmation_message(
            self.request, self.object
        )

    @staticmethod
    def __get_form_from_registration_formset(
            registration_formset: BaseInlineFormSet) -> UserRoleApplication:
        forms = registration_formset.save(commit=False)
        if len(forms) == 1:
            return forms[0]
        raise ValueError('only one user is supposed to be in this formset')


@login_required
def index_view(request: HttpRequest):
    if request.user.is_authenticated and request.user.is_admin:  # noqa
        return redirect(reverse_lazy('admin_page'))
    return render(request, 'index.html')


def successfully_created_registration_request(request):
    return render(request, 'registration/successfully_created_registration_request.html')


class ConfirmEmail(View):
    def post(self, request, user_id: int, user_email: str):  # noqa
        EmailConfirmationController.confirm_email_if_user_exists_or_404(user_id, user_email)
        messages.success(
            request,
            _('Пошту успішно підтверджено')
        )
        return redirect('successfully_confirmed_email')

    def get(self, request):  # noqa
        return render(request, 'registration/successfully_confirmed_email.html')
