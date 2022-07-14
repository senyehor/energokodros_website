from django.urls import path

from administrator import views

urlpatterns = [
    path(
        '',
        views.admin_page,
        name='admin_page'
    ),
    path(
        'users-roles-applications/',
        views.UserRoleApplicationsListView.as_view(),
        name='users_roles_applications'
    ),
    path(
        'users-roles-applications/<hashed_int:pk>',
        views.UserRoleApplicationDecisionView.as_view(),
        name='user_role_application'
    ),
]
