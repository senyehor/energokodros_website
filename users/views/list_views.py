from users.logic.simple import (
    get_applications_from_users_who_confirmed_email,
    get_users_with_confirmed_email,
)
from users.models import UserRole
from utils.common import admin_rights_and_login_required
from utils.views import ListViewWithFiltering


@admin_rights_and_login_required
class UserRoleApplicationsListView(ListViewWithFiltering):
    queryset = get_applications_from_users_who_confirmed_email()
    filter_fields = ('user__full_name', 'user__email', 'institution__name')
    template_name = 'users/users_roles_applications.html'


@admin_rights_and_login_required
class UserListView(ListViewWithFiltering):
    queryset = get_users_with_confirmed_email()
    filter_fields = ('full_name', 'email')
    template_name = 'users/users_list.html'


@admin_rights_and_login_required
class UserRoleListView(ListViewWithFiltering):
    queryset = UserRole.objects.all()
    filter_fields = ('facility_has_access_to__name', 'user__full_name', 'position_name')
    template_name = 'users/users_roles_list.html'
