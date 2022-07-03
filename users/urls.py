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
        name='successfully_created_registration_request'
    ),
    path(
        'confirm-email/<hashed_int:user_id>/<hashed_string:user_email>',
        views.confirm_email,
        name='confirm_email'
    ),
    path(
        'successfully-confirmed-email',
        views.successfully_confirmed_email,
        name='successfully_confirmed_email'
    )
]
urlpatterns.append(path('', include('django.contrib.auth.urls')))
