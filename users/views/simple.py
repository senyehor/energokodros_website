from django.contrib import messages
from django.contrib.auth.views import LoginView as LogView
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import UpdateView

from users.forms import EditUserForm, LoginForm
from users.logic import remember_user_for_two_week, UserRegistrationController
from users.models import User


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


class EditUserView(UpdateView):
    model = User
    form_class = EditUserForm
    success_url = reverse_lazy('users-list')
    template_name = 'administrator/edit-user.html'
    # overriden due to 'user' taken by client user variable
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        data['form'].fill_querysets(user)
        return data

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Користувача успішно відредаговано')
        )
        return super().form_valid(form)


class ProfilesView(View):
    """currently it is just a stub"""

    def get(self, request):
        return render(request, 'index.html')
