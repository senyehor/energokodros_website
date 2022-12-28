from .create_user_registration_request import CreateUserRegistrationRequestView
from .edit_views import EditUserRoleView, EditUserView
from .list_views import UserListView, UserRoleApplicationsListView, UserRoleListView
from .simple import (
    confirm_email, LoginView, ProfileView, RoleApplicationView,
    successfully_created_registration_request,
)
from .user_role_application_decision import UserRoleApplicationDecisionView
