from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as LogView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from users.decorators import admin
from users.forms import (
    LoginForm,
    NewUserForm,
    UserRegistrationRequestFormset,
    UserRegistrationRequestsDecisionForm
)
from users.logic import remember_user_for_two_week
from users.models import UserRole, UserRegistrationRequest


class LoginView(LogView):
    authentication_form = LoginForm

    def form_valid(self, form):
        if form.data.get('remember_me'):
            remember_user_for_two_week(self.request, )
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
        return redirect(reverse_lazy('successfully_created_registration_request'))

    def form_invalid(  # noqa pylint: pylint: disable=W0221
            self, form: NewUserForm,
            user_registration_request_formset: UserRegistrationRequestFormset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                user_registration_request_formset=user_registration_request_formset,
            ),
            status=400
        )


@login_required
def index_view(request: HttpRequest):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect(reverse_lazy('admin_page'))
    return render(request, 'index.html')


def successfully_created_registration_request(request):
    return render(request, 'index.html')
