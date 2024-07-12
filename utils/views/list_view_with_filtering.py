from typing import Iterable, TypeAlias, Union

from django.db.models import Q, QuerySet
from django.views.generic import ListView

from utils.types import StrTuple

_ListViewWithMixinType: TypeAlias = Union[ListView, '_QuerySetFieldsIcontainsFilterPkOrderedMixin']
DEFAULT_PAGINATE_BY = 7


class QuerySetFieldsIcontainsFilter:
    def __init__(self, qs: QuerySet, fields_to_filter: Iterable[str]):
        self.__qs = qs
        self.__fields_to_filter = [f'{field}__icontains' for field in fields_to_filter]

    def filter(self, value: str) -> QuerySet:
        q_filters = Q()
        for field in self.__fields_to_filter:
            q_filters = q_filters | Q(**{field: value})
        return self.__qs.filter(q_filters)


class _QuerySetFieldsIcontainsFilterPkOrderedMixin:
    """this mixin is supposed to be used with ListViews"""
    filter_fields: StrTuple = None
    fields_order_by_before_pk: StrTuple = tuple()
    __filter = QuerySetFieldsIcontainsFilter

    def get_queryset(self: _ListViewWithMixinType) -> QuerySet:
        if search_value := self.__get_search_value():
            qs = self.__filter_queryset_for_value(search_value)
        else:
            qs = self.queryset
        return qs.order_by(*self.fields_order_by_before_pk, '-pk')

    def __filter_queryset_for_value(self: _ListViewWithMixinType, value: str) -> QuerySet:
        return self.__filter(
            self.queryset,
            self.filter_fields,
        ).filter(value)

    def __get_search_value(self: ListView) -> str:
        return self.request.GET.get('search_value', None)


class ListViewWithFiltering(_QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    paginate_by = DEFAULT_PAGINATE_BY
