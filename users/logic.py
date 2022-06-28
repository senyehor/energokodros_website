from dataclasses import dataclass
from datetime import timedelta
from hashlib import sha256
from typing import Callable

from django.forms import BaseInlineFormSet
from django.http import HttpRequest


@dataclass
class UserRegistrationCode:
    __algorithm: Callable[[bytes], str] = sha256
    LENGTH = 64  #

    @classmethod
    def generate(cls, email: str) -> str:
        return cls.__algorithm(email.encode()).hexdigest()


def remember_user_for_two_week(request: HttpRequest):
    _remember_user_for_timedelta(request, timedelta(weeks=2))


def _remember_user_for_timedelta(request: HttpRequest, td: timedelta):
    request.session.set_expiry(td)


def _get_user_registration_formset(formset: BaseInlineFormSet) \
        -> BaseInlineFormSet:
    # formsets are supposed to work with bulk data, but we just need it to
    # join NewUser + UserRegistrationRequestForm in quantity 1, so we fearlessly take [0]
    return formset.save(commit=False)[0]


def _generate_code_for_email(email: str) -> str:
    return UserRegistrationCode.generate(email)
