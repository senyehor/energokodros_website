from .create_user_registration_request import CreateUserRegistrationRequestView
from .list_views import UserListView, UserRoleApplicationsListView, UserRoleListView
from .simple import (
    confirm_email, LoginView, ProfileView, RoleApplicationView,
    successfully_created_registration_request, UserRoleView, UserView,
)
from .user_role_application_decision import UserRoleApplicationDecisionView
