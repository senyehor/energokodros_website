from datetime import timedelta

from django import forms
from django.contrib.auth.views import LoginView as LogView
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginForm, NewUserForm, UserRegistrationRequestFormset


class LoginView(LogView):
    form_class = LoginForm
    remember_me = forms.BooleanField(required=False, label="Запам'ятати мене на два тижні")

    def form_valid(self, form):
        if form.data.get('remember_me'):
            self.request.session.set_expiry(timedelta(weeks=2))
        return super().form_valid(form)


class CreateUserRegistrationRequest(CreateView):
    form_class = NewUserForm
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_registration_request_formset'] = UserRegistrationRequestFormset()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None  # noqa
        form = self.get_form(self.get_form_class())
        user_registration_request_formset = UserRegistrationRequestFormset(self.request.POST)
        if form.is_valid() and user_registration_request_formset.is_valid():
            return self.form_valid(form, user_registration_request_formset)
        return self.form_invalid(form, user_registration_request_formset)

    def form_valid(  # noqa pylint: disable=W0221
            self, form: NewUserForm,
            user_registration_request_formset: UserRegistrationRequestFormset):
        self.object = form.save(commit=False)  # noqa
        self.object.save()
        # formsets are supposed to work with bulk data, but we just need it to
        # join NewUser + UserRegistrationRequestForm in quantity 1, so we fearlessly take [0]
        form = user_registration_request_formset.save(commit=False)[0]
        form.user = self.object
        form.save()
        return redirect(reverse_lazy('home'))

    def form_invalid(  # noqa pylint: pylint: disable=W0221
            self, form: NewUserForm,
            user_registration_request_formset: UserRegistrationRequestFormset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                user_registration_request_formset=user_registration_request_formset
            )
        )


def index_view(request: HttpRequest):
    return render(request, 'index.html')
