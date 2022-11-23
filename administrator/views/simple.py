from django.views.generic import ListView, TemplateView

from administrator.logic import (
    admin_rights_required,
    get_applications_from_users_who_confirmed_email, get_users_with_confirmed_email,
)
from energokodros.settings import DEFAULT_PAGINATE_BY
from utils.filters import QuerySetFieldsIcontainsFilterPkOrderedMixin


@admin_rights_required
class AdminPageView(TemplateView):
    template_name = 'administrator/administrator.html'


@admin_rights_required
class UserRoleApplicationsListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = get_applications_from_users_who_confirmed_email()
    filter_fields = ('user__full_name', 'user__email', 'institution__name')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'administrator/users_roles_applications.html'


@admin_rights_required
class UserListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = get_users_with_confirmed_email()
    filter_fields = ('full_name', 'email')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'administrator/users_list.html'
