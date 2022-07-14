from django.urls import path

from administrator import views

urlpatterns = [
    path(
        '',
        views.admin_page,
        name='admin-page'
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
]
