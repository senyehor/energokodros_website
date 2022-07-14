from django.urls import include, path

from users import views

urlpatterns = [  # noqa
    path('login/', views.LoginView.as_view()),
    path(
        'registration/',
        views.CreateUserRegistrationRequest.as_view(),
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
        'successfully-confirmed-email',
        views.successfully_confirmed_email,
        name='successfully-confirmed-email'
    ),
    path(
        'profiles/',
        views.ProfilesView.as_view(),
        name='profiles'
    )
]
urlpatterns.append(path('', include('django.contrib.auth.urls')))
