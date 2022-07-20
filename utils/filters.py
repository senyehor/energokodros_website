from functools import reduce
from typing import Iterable

from django.db.models import Q, QuerySet
from django.views.generic import ListView


class QuerySetFieldsIcontainsFilterPkOrderedMixin:
    filter_fields = None
    """this mixin is supposed to be used with ListViews"""

    def get_queryset(self) -> QuerySet:
        self.__check_used_properly()
        if search_value := self.__get_search_value():
            return QuerySetFieldsIcontainsFilterPkOrdered(
                self.queryset,  # noqa
                self.filter_fields,
            ).filter(search_value)
        return self.queryset  # noqa

    def __check_used_properly(self):
        if not isinstance(self, ListView):
            raise ValueError('this mixin must be used with a ListView')
        if self.filter_fields is None:  # noqa
            raise ValueError('you must set filter_fields for queryset')
        return True

    def __get_search_value(self) -> str:
        return self.request.GET.get('search_value', None)  # noqa


class QuerySetFieldsIcontainsFilterPkOrdered:
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
