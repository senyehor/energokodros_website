from django.urls import include, path

from administrator import views

urlpatterns = [
    path(
        '',
        views.AdminPageView.as_view(),
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
    path(
        'users-list/',
        views.UserListView.as_view(),
        name='users-list'
    ),
    path('', include('institutions.urls')),
]
