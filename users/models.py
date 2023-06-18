from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.utils import _full_name_validator

USER_FULL_NAME_MAX_LENGTH = 150


class UserManager(BaseUserManager):
    def create(self, password: str, ):
        pass


class User(AbstractBaseUser):
    full_name = models.CharField(
        _("повне ім'я"),
        max_length=USER_FULL_NAME_MAX_LENGTH,
        validators=[_full_name_validator]
    )
    email = models.EmailField(_('електронна пошта'), unique=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'
