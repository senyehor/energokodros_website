from typing import Iterable

from django import template
from django.core.paginator import Paginator
from django.http import HttpRequest

from utils.templatetags.url_replace import url_replace

register = template.Library()

START_PAGE_NUMBER = 1
SIDE_NEIGHBOR_COUNT = 5
MAX_NEIGHBOR_COUNT = SIDE_NEIGHBOR_COUNT * 2
TOTAL_PAGE_ITEMS_COUNT = MAX_NEIGHBOR_COUNT + 1

INVISIBLE_PAGE_DELTA = SIDE_NEIGHBOR_COUNT + 1


class StartAndEndPagesIndexes:

    def __init__(self, current_page_number: int, num_pages: int):
        self.__start = max(START_PAGE_NUMBER, current_page_number - SIDE_NEIGHBOR_COUNT)
        self.__end = min(num_pages, current_page_number + SIDE_NEIGHBOR_COUNT)
        self.__num_pages = num_pages

    def get_pages_indexes(self) -> Iterable[int]:
        self.__expand_pages_indexes_boundaries_if_needed()
        self.__shrink_pages_indexes_boundaries_if_needed()
        return self.__create_pages_indexes()

    def __create_pages_indexes(self) -> Iterable[int]:
        return range(self.__start, self.__end + 1)[:TOTAL_PAGE_ITEMS_COUNT]

    def __expand_pages_indexes_boundaries_if_needed(self):
        if self.__check_end_less_than_start_plus_max_neighbor_count():
            self.__set_end_to_start_plus_max_neighbor_count()
        elif self.__check_start_greater_than_end_minus_max_neighbor_count():
            self.__set_start_to_end_minus_max_neighbor_count()

    def __shrink_pages_indexes_boundaries_if_needed(self):
        if self.__start < START_PAGE_NUMBER:
            self.__end -= self.__start
            self.__start = START_PAGE_NUMBER
        elif self.__end > self.__num_pages:
            self.__end = self.__num_pages

    def __check_end_less_than_start_plus_max_neighbor_count(self) -> bool:
        return self.__end < self.__start_plus_max_neighbor_count

    def __set_end_to_start_plus_max_neighbor_count(self):
        self.__end = self.__start_plus_max_neighbor_count

    def __check_start_greater_than_end_minus_max_neighbor_count(self) -> bool:
        return self.__start > self.__end_minus_max_neighbor_count

    def __set_start_to_end_minus_max_neighbor_count(self):
        self.__start = self.__end_minus_max_neighbor_count

    @property
    def __start_plus_max_neighbor_count(self) -> int:
        return self.__start + MAX_NEIGHBOR_COUNT

    @property
    def __end_minus_max_neighbor_count(self) -> int:
        return self.__end - MAX_NEIGHBOR_COUNT


@register.filter(name='paginate_with_items_per_page_limit')
def paginate_with_items_per_page_limit(paginator: Paginator, current_page_number: int):
    if __check_pages_need_to_be_shortened(paginator.num_pages):
        indexes = StartAndEndPagesIndexes(current_page_number, paginator.num_pages)
        return indexes.get_pages_indexes()
    return paginator.page_range


@register.simple_tag
def next_invisible_page_number_if_exists_else_max_available_link(
        request: HttpRequest, page_number: int, num_pages: int) -> str:
    next_invisible_page_number = page_number + INVISIBLE_PAGE_DELTA
    if next_invisible_page_number < num_pages:
        page_to_redirect_to = next_invisible_page_number
    else:
        page_to_redirect_to = num_pages
    return url_replace(request, 'page', page_to_redirect_to)


@register.simple_tag
def previous_invisible_page_number_if_exists_else_min_available_link(
        request: HttpRequest, page_number: int) -> str:
    previous_invisible_page_number = page_number - INVISIBLE_PAGE_DELTA
    if previous_invisible_page_number < START_PAGE_NUMBER:
        page_to_redirect_to = START_PAGE_NUMBER
    else:
        page_to_redirect_to = previous_invisible_page_number
    return url_replace(request, 'page', page_to_redirect_to)


def __check_pages_need_to_be_shortened(num_pages: int) -> bool:
    return num_pages > MAX_NEIGHBOR_COUNT
