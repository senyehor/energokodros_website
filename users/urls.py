from django.urls import include, path

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
    ),
    path('', include('django.contrib.auth.urls')),
]

ajax_urls = [
    path(
        'edit-user-role-pk-in-post',
        views.redirect_to_edit_role_by_post_pk,
        name='edit-user-role-pk-in-post'
    ),
]

urlpatterns += ajax_urls
