from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as LogView
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import FormView

from users.forms import LoginForm, ProfileForm
from users.logic import remember_user_for_two_week, UserRegistrationController
from utils.common.decoration import decorate_class_or_function_view


def successfully_created_registration_request(request):
    return render(request, 'registration/successfully_created_registration_request.html')


def confirm_email(request: HttpRequest, user_id: int, user_email: str):
    UserRegistrationController.confirm_email_if_user_exists(user_id, user_email)
    return render(request, 'registration/successfully_confirmed_email.html')


class LoginView(LogView):
    authentication_form = LoginForm

    def form_valid(self, form):
        if form.data.get('remember_me'):
            remember_user_for_two_week(self.request)
        return super().form_valid(form)


@decorate_class_or_function_view(login_required)
class ProfileView(FormView):
    form_class = ProfileForm
    template_name = 'users/profile.html'

    def get_form(self, form_class=None):
        return self.form_class(user=self.request.user)
