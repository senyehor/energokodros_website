from .create_user_registration_request import CreateUserRegistrationRequestView
from .simple import (
    confirm_email, EditUserRoleView, EditUserView, LoginView, redirect_to_edit_role_by_post_pk,
    successfully_created_registration_request, UserListView, UserRoleApplicationsListView,
    UserRoleListView,
)
from .user_role_application_decision import UserRoleApplicationDecisionView
