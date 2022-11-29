from django.views.generic import ListView

from energokodros.settings import DEFAULT_PAGINATE_BY
from users.logic.simple import (
    get_applications_from_users_who_confirmed_email,
    get_users_with_confirmed_email,
)
from users.models import UserRole
from utils.common import admin_rights_required
from utils.list_view_filtering import QuerySetFieldsIcontainsFilterPkOrderedMixin


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
