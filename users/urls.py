from django.urls import include, path

from institutions.urls import helper_urls
from users import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path(
        'registration/',
        views.CreateUserRegistrationRequestView.as_view(),
        name='register'
    ),
    path(
        'successfully-created-registration-request/',
        views.successfully_created_registration_request,
        name='successfully-created-registration-request'
    ),
    path(
        'confirm-email/<hashed_int:user_id>/<hashed_str:user_email>/',
        views.confirm_email,
        name='confirm-email'
    ),
    path('', include('django.contrib.auth.urls'))
]

admin_urls = [
    path(
        'users-roles-applications/',
        views.UserRoleApplicationsListView.as_view(),
        name='users-roles-applications'
    ),
    path(
        'user-role-application-decision/<hashed_int:pk>',
        views.UserRoleApplicationDecisionView.as_view(),
        name='user-role-application-decision'
    ),
    path(
        'users-list/',
        views.UserListView.as_view(),
        name='users-list'
    ),
    path(
        'edit-user/<hashed_int:pk>/',
        views.EditUserView.as_view(),
        name='edit-user'
    ),
    path(
        'users-roles-list/',
        views.UserRoleListView.as_view(),
        name='users-roles-list'
    ),
    path(
        'edit-user-role/<hashed_int:pk>/',
        views.EditUserRoleView.as_view(),
        name='edit-user-role'
    )
]

urlpatterns += admin_urls

