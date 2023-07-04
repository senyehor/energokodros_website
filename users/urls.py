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
        'confirm-email/<hashed_int:user_id>/<hashed_str:email>/',
        views.ConfirmEmail.as_view(),
        name='confirm_email'
    ),
    path(
        'successfully-confirmed-email',
        views.ConfirmEmail.as_view(),
        name='successfully_confirmed_email'
    )
]
urlpatterns.append(path('', include('django.contrib.auth.urls')))
