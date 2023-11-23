from django.urls import include, path

from administrator import views
from users import views as users_views

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
    # todo organize
    path(
        'edit-user/<hashed_int:pk>/',
        users_views.EditUserView.as_view(),
        name='edit-user'
    ),
    path('', include('institutions.urls')),
]
