from django.utils.translation import gettext_lazy as _
from django.db import models

from institutions.models import Institution
from users.models import User


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
