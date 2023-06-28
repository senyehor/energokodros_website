from datetime import timedelta

from django.forms import BaseInlineFormSet
from django.http import HttpRequest

from users.forms import UserRegistrationRequestFormset


def remember_user_for_two_week(request: HttpRequest):
    _remember_user_for_timedelta(request, timedelta(weeks=2))


def _remember_user_for_timedelta(request: HttpRequest, td: timedelta):
    request.session.set_expiry(td)


def _get_user_registration_formset(formset: BaseInlineFormSet) \
        -> BaseInlineFormSet:
    # formsets are supposed to work with bulk data, but we just need it to
    # join NewUser + UserRegistrationRequestForm in quantity 1, so we fearlessly take [0]
    return formset.save(commit=False)[0]
