from enum import Enum

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import UserRoleApplicationRequestsDecisionForm
from users.logic import check_user_has_no_roles, UserRoleApplicationReviewController
from users.models import UserRoleApplication
from utils.common import admin_rights_required


class DECISIONS(str, Enum):
    DECISION_ARGUMENT = 'decision'
    ACCEPT = 'accept'
    DECLINE = 'decline'


@admin_rights_required
class UserRoleApplicationDecisionView(FormView):
    template_name = 'users/user_role_application_decision.html'
    form_class = UserRoleApplicationRequestsDecisionForm
    success_url = reverse_lazy('users-roles-applications')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_has_no_roles'] = check_user_has_no_roles(self.__get_application_request().user)
        return ctx

    def get_form(self, form_class=None):
        return UserRoleApplicationReviewController.get_application_decision_form_for_application(
            self.__get_application_request()
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if self.__application_approved_but_form_invalid(form):
            return self.form_invalid(form)
        # noinspection PyAttributeOutsideInit
        self.controller = UserRoleApplicationReviewController(
            form,
            self.__get_application_request(),
            self.request,
            self.is_application_approved
        )
        return self.form_valid(form)

    def form_valid(self, form):
        self.controller.process_depending_on_decision()
        return super().form_valid(form)

    def __get_application_request(self):
        return get_object_or_404(UserRoleApplication, pk=self.kwargs['pk'])

    def __application_approved_but_form_invalid(
            self, form: UserRoleApplicationRequestsDecisionForm):
        return self.is_application_approved and not form.is_valid()

    @property
    def is_application_approved(self):
        return self.request.POST[DECISIONS.DECISION_ARGUMENT] == DECISIONS.ACCEPT

    @property
    def is_application_declined(self):
        return not self.is_application_approved
