from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from users.forms import EditUserForm, EditUserRole
from users.models import User, UserRole
from utils.common import admin_rights_required
from utils.forms import EditObjectUpdateViewMixin


@admin_rights_required
class EditUserRoleView(EditObjectUpdateViewMixin, UpdateView):
    model = UserRole
    form_class = EditUserRole
    success_url = reverse_lazy('users-roles-list')
    template_name = 'users/edit_user_role.html'

    edit_success_message = _('Роль користувача успішно відредаговано')


@admin_rights_required
class EditUserView(EditObjectUpdateViewMixin, UpdateView):
    model = User
    form_class = EditUserForm
    success_url = reverse_lazy('users-list')
    template_name = 'users/edit_user.html'
    # overriden due to 'user' taken by client user variable
    context_object_name = 'user_obj'

    edit_success_message = _('Користувача успішно відредаговано')
