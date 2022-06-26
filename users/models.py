from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _

from institutions.models import AccessLevel, Institution
from users.utils import _full_name_validator


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
        max_length=150,
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
    is_admin = models.BooleanField(
        _('чи є адміністратором'),
        default=False,
        null=False
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return _(self.full_name)


class UserRole(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='roles'
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='users_roles'
    )
    access_level = models.ForeignKey(
        AccessLevel,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        related_name='+'
    )
    position = models.CharField(
        _('посада'),
        max_length=255,
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'users_roles'

    def __str__(self):
        return _(f'{self.position} {self.user.full_name} в {self.institution}')


class UserRegistrationRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='registration_requests'
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='+'
    )
    message = models.TextField(
        _("повідомлення від користувача"),
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'users_registration_requests'

    def __str__(self):
        return _(f'Запит на реєстрацію від {self.user.full_name} в {str(self.institution)}')
