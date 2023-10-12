from datetime import timedelta

from django.http import HttpRequest


def remember_user_for_two_week(request: HttpRequest):
    __remember_user_for_timedelta(request, timedelta(weeks=2))


def __remember_user_for_timedelta(request: HttpRequest, td: timedelta):
    request.session.set_expiry(td)
