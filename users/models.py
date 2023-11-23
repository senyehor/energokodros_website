from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

from institutions.models import Facility
from users.utils import _full_name_validator


class UserManager(BaseUserManager):
    def create(self, full_name: str, email: str, password: str,
               is_admin: bool = False, is_active: bool = False) -> 'User':
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, is_admin=is_admin, is_active=is_active)
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
        blank=False,
        error_messages={
            'unique': _('Користувач із такою поштою вже існує'),
        }
    )
    is_admin = models.BooleanField(
        _('чи є адміністратором'),
        default=False,
        null=False
    )
    is_active = models.BooleanField(
        _('чи підтвердив користувач пошту'),
        null=False,
        default=False
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('edit-user', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'users'
        verbose_name = _('Користувач')
        verbose_name_plural = _('Користувачі')

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
    facility_has_access_to = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='users_roles'
    )
    position_name = models.CharField(
        _('Назва посади'),
        max_length=255,
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'users_roles'
        verbose_name = _('Роль користувача')
        verbose_name_plural = _('Ролі користувача')

    def __str__(self):
        return _(f'{self.position_name}')


class UserRoleApplication(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='registration_requests'
    )
    institution = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='+'
    )
    message = models.TextField(
        _('повідомлення від користувача'),
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'users_roles_applications'
        verbose_name = _('Запит на отримання ролі користувачем')
        verbose_name_plural = _('Запити на отримання ролі користувачів')

    def __str__(self):
        return _(f'Запит на реєстрацію від {self.user.full_name} в {self.institution}')

    def get_absolute_url(self):
        return reverse('user-role-application-decision', kwargs={'pk': self.pk})
