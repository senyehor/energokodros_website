from django.contrib.auth.views import LoginView as LogView
from django.contrib.auth.views import LoginView as LogView
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView

from energokodros.settings import DEFAULT_PAGINATE_BY
from users.forms import EditUserForm, EditUserRole, LoginForm
from users.logic import remember_user_for_two_week, UserRegistrationController
from users.logic.simple import (
    get_applications_from_users_who_confirmed_email,
    get_users_with_confirmed_email,
)
from users.models import User, UserRole
from utils.common.admin_rights import admin_rights_required
from utils.forms import EditObjectUpdateViewMixin
from utils.list_view_filtering import QuerySetFieldsIcontainsFilterPkOrderedMixin


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


@admin_rights_required
class EditUserView(EditObjectUpdateViewMixin, UpdateView):
    model = User
    form_class = EditUserForm
    success_url = reverse_lazy('users-list')
    template_name = 'users/edit_user.html'
    # overriden due to 'user' taken by client user variable
    context_object_name = 'user_obj'

    edit_success_message = _('Користувача успішно відредаговано')


@admin_rights_required
class EditUserRoleView(EditObjectUpdateViewMixin, UpdateView):
    model = UserRole
    form_class = EditUserRole
    success_url = reverse_lazy('users-roles-list')
    template_name = 'users/edit_user_role.html'

    edit_success_message = _('Роль користувача успішно відредаговано')


@admin_rights_required
class UserRoleApplicationsListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = get_applications_from_users_who_confirmed_email()
    filter_fields = ('user__full_name', 'user__email', 'institution__name')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'users/users_roles_applications.html'


@admin_rights_required
class UserListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = get_users_with_confirmed_email()
    filter_fields = ('full_name', 'email')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'users/users_list.html'


@admin_rights_required
class UserRoleListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = UserRole.objects.all()
    filter_fields = ('facility_has_access_to__name', 'user__full_name', 'position_name')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'users/users_roles_list.html'
