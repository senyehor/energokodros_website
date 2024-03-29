from functools import reduce
from typing import Iterable, TypeAlias, Union

from django.db.models import Q, QuerySet
from django.views.generic import ListView

from utils.types import StrTuple

_ListViewWithMixinType: TypeAlias = Union[ListView, 'QuerySetFieldsIcontainsFilterPkOrderedMixin']
DEFAULT_PAGINATE_BY = 7


class QuerySetFieldsIcontainsFilterPkOrderedMixin:
    """this mixin is supposed to be used with ListViews"""
    filter_fields: StrTuple = None
    fields_order_by_before_pk: StrTuple = set()

    def get_queryset(self: _ListViewWithMixinType) -> QuerySet:
        self.__check_used_properly()
        if search_value := self.__get_search_value():
            qs = QuerySetFieldsIcontainsFilter(
                self.queryset,
                self.filter_fields,
            ).filter(search_value)
        else:
            qs = self.queryset
        return qs.order_by(*self.fields_order_by_before_pk, '-pk')

    def __check_used_properly(self: _ListViewWithMixinType):
        if not issubclass(self.__class__, ListView):
            raise ValueError('this mixin must be used with a ListView')
        if self.filter_fields is None:
            raise ValueError('you must set filter_fields for a model')
        return True

    def __get_search_value(self: ListView) -> str:
        return self.request.GET.get('search_value', None)


class QuerySetFieldsIcontainsFilter:
    def __init__(self, qs: QuerySet, fields_to_filter: Iterable[str]):
        self._qs = qs
        self._fields_to_filter = [f'{field}__icontains' for field in fields_to_filter]

    def filter(self, value: str) -> QuerySet:
        _filter = reduce(
            lambda q, field: q | Q(**{field: value}),
            self._fields_to_filter,
            Q()
        )
        return self._qs.filter(_filter)


class ListViewWithFiltering(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    paginate_by = DEFAULT_PAGINATE_BY
    pass
