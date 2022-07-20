from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView

from administrator.decorators import admin_rights_required
from administrator.logic import get_applications_from_users_who_confirmed_email_ordered
from energokodros.settings import DEFAULT_PAGINATE_BY
from utils.filters import QuerySetFieldsIcontainsFilterPkOrderedMixin


@admin_rights_required
def admin_page(request: HttpRequest):
    return render(
        request,
        'administrator/administrator.html',
    )


@admin_rights_required
class UserRoleApplicationsListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = get_applications_from_users_who_confirmed_email_ordered()
    filter_fields = ('user__full_name', 'user__email', 'institution__name')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'administrator/users_roles_applications.html'
