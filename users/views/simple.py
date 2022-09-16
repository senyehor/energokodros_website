from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as LogView
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from administrator.logic import is_admin
from users.forms import LoginForm
from users.logic import remember_user_for_two_week, UserRegistrationController


@login_required
def index_view(request: HttpRequest):
    if is_admin(request):
        return redirect(reverse('admin-page'))
    return render(request, 'index.html')


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


class ProfilesView(View):
    """currently it is just a stub"""

    def get(self, request):
        return render(request, 'index.html')