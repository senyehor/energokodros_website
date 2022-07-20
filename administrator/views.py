from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView

from administrator.decorators import admin_rights_required
from administrator.forms import UserRoleApplicationRequestsDecisionForm
from administrator.logic import (
    check_user_has_no_roles,
    get_applications_from_users_who_confirmed_email_ordered,
    UserRoleApplicationReviewController
)
from energokodros.settings import DEFAULT_PAGINATE_BY
from users.models import UserRoleApplication
from utils.filters import QuerySetFieldsIcontainsFilterPkOrderedMixin


@admin_rights_required
def admin_page(request: HttpRequest):
    return render(
        request,
        'administrator/administrator.html',
    )


@admin_rights_required
class UserRoleApplicationsListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = get_applications_from_users_who_confirmed_email_ordered()
    filter_fields = ('user__full_name', 'user__email', 'institution__name')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'administrator/users_roles_applications.html'


@admin_rights_required
class UserRoleApplicationDecisionView(FormView):
    template_name = 'administrator/user_role_application_decision.html'
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
        self.controller = UserRoleApplicationReviewController(
            form,
            self.__get_application_request(),
            self.request,
            self.application_approved
        )
        valid = self.controller.validate_form()
        return self.form_valid(form) if valid else self.form_invalid(form)

    def form_valid(self, form: UserRoleApplicationRequestsDecisionForm):
        self.controller.process_depending_on_decision()
        return redirect(reverse('users-roles-applications'))

    def __get_application_request(self):
        return get_object_or_404(UserRoleApplication, pk=self.kwargs['pk'])

    @property
    def application_approved(self):
        return self.request.POST['decision'] == 'accept'

    @property
    def application_declined(self):
        return not self.application_approved
