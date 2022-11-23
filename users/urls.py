from django.urls import include, path

from users import views

urlpatterns = [  # noqa
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
        'profiles/',
        views.ProfilesView.as_view(),
        name='profiles'
    ),
    path('', include('django.contrib.auth.urls'))
]
