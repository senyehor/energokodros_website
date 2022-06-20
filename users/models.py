from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.utils import _full_name_validator

USER_FULL_NAME_MAX_LENGTH = 150


class UserManager(BaseUserManager):
    def create(self, full_name: str, email: str, password: str, is_admin: bool = False) -> 'User':
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, is_admin=is_admin)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(
        _("повне ім'я"),
        max_length=USER_FULL_NAME_MAX_LENGTH,
        validators=[_full_name_validator],
        null=False,
        blank=False
    )
    email = models.EmailField(
        _('електронна пошта'),
        unique=True,
        null=False,
        blank=False
    )
    is_admin = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'users'
