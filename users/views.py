from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as LogView
from django.forms import BaseInlineFormSet
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import (
    LoginForm,
    NewUserForm,
    RegistrationFormset
)
from users.logic import RegistrationController, remember_user_for_two_week
from users.models import User


class LoginView(LogView):
    authentication_form = LoginForm

    def form_valid(self, form):
        if form.data.get('remember_me'):
            remember_user_for_two_week(self.request)
        return super().form_valid(form)


class CreateUserRegistrationRequest(CreateView):
    form_class = NewUserForm
    template_name = 'registration/register.html'
    controller = RegistrationController

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

    def form_valid(self, form: NewUserForm, registration_formset: RegistrationFormset):  # noqa pylint: disable=W0221
        self.object = form.save(commit=False)  # noqa
        self.object.save()
        form = self.__get_user_from_registration_formset(registration_formset)
        form.user = self.object
        form.save()
        return redirect(reverse_lazy('home'))

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

    @staticmethod
    def __get_user_from_registration_formset(registration_formset: BaseInlineFormSet) -> User:
        # here we take [0], as formset is supposed to work with bulk data,
        # but is used here to join user creating from and user role application form
        return registration_formset.save(commit=False)[0]


@login_required
def index_view(request: HttpRequest):
    if request.user.is_authenticated and request.user.is_admin:  # noqa
        return redirect(reverse_lazy('admin_page'))
    return render(request, 'index.html')


def successfully_created_registration_request(request: HttpRequest):
    return render(request, 'successfully_created_registration_request.html')
