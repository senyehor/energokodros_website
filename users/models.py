from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models, transaction
from django.utils.translation import gettext as _

from institutions.models import AccessLevel, Institution
from users.logic import UserRegistrationCode
from users.utils import _full_name_validator


class UserManager(BaseUserManager):
    def create(self, full_name: str, email: str, password: str, is_admin: bool = False) -> 'User':
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, is_admin=is_admin)
        user.set_password(password)
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

    USERNAME_FIELD = 'email'

    objects = UserManager()

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
        verbose_name = _('Роль користувача')
        verbose_name_plural = _('Ролі користувача')

    def __str__(self):
        return _(f'{self.position} {self.user.full_name} в {self.institution}')


class UserRegistrationDataManager(UserManager):
    def create(self, full_name: str, email: str, password: str, is_admin: bool = False,
               email_code: str = None, email_confirmed: bool = False,
               applied_at: datetime = None) -> 'UserRegistrationData':
        user = super().create(full_name, email, password, is_admin)
        if applied_at is None:
            applied_at = datetime.now()
        return self.model(
            full_name=user.full_name,
            email=user.email,
            password=user.password,
            is_admin=user.is_admin,
            email_code=email_code,
            email_confirmed=email_confirmed,
            applied_at=applied_at
        )


class UserRegistrationData(User):
    # we do not care about storing non-confirmed user`s data in User model, as
    # we will operate user roles (non-confirmed user can not have a role)
    email_code = models.CharField(
        _('код верифікації пошти'),
        max_length=UserRegistrationCode.LENGTH,
        null=False
    )
    email_confirmed = models.BooleanField(
        _('чи підтвердив користувач реєстрацію'),
        null=False,
        default=False
    )
    applied_at = models.DateTimeField(
        _('дата подання заяви'),
        null=False,
        auto_now_add=True
    )

    objects = UserRegistrationDataManager()

    def confirm_email(self):
        self.email_confirmed = True
        self.save()

    def review_registration(self, accepted: bool = False, is_admin: bool = False):
        with transaction.atomic():
            if accepted:
                # here we provide empty password and set it explicitly later, as
                # user registration data already has password, and it is already encrypted,
                # so we can set it following way
                user = User.objects.create(
                    self.full_name,
                    email=self.email,
                    password='',
                    is_admin=is_admin
                )
                user.password = self.password
                user.save()
            self.delete()

    class Meta:
        db_table = 'users_registration_data'
        verbose_name = _('Дані реєстрації користувача')
        verbose_name_plural = verbose_name


class UserRoleApplication(models.Model):
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
        db_table = 'users_role_applications'
        verbose_name = _('Запит на отримання ролі користувачем')
        verbose_name_plural = _('Запити на отримання ролі користувачів')

    def __str__(self):
        return _(f'Запит на реєстрацію від {self.user.full_name} в {str(self.institution)}')
