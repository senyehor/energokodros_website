from django.views.generic import ListView

from administrator.decorators import admin_rights_required
from energokodros.settings import DEFAULT_PAGINATE_BY
from institutions.models import AccessLevel
from utils.filters import QuerySetFieldsIcontainsFilterPkOrderedMixin


@admin_rights_required
class AccessLevelListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = AccessLevel.objects.all()
    filter_fields = ('code', 'description')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'institution/access_levels_list.html'
