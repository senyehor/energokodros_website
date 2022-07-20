from django.urls import path

import administrator.views

urlpatterns = [
    path(
        '',
        administrator.views.admin_page,
        name='admin-page'
    ),
    path(
        'users-roles-applications/',
        administrator.views.UserRoleApplicationsListView.as_view(),
        name='users-roles-applications'
    ),
    path(
        'user-role-application-decision/<hashed_int:pk>',
        administrator.views.UserRoleApplicationDecisionView.as_view(),
        name='user-role-application-decision'
    ),
]
