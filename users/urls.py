from django.urls import include, path

from users import views

# using /? to override some of django.contrib.auth.urls
overridden_account_patterns = [
    path('login/', views.LoginView.as_view()),
]

urlpatterns = overridden_account_patterns + [
    path(
        'registration/',
        views.CreateUserRegistrationRequest.as_view(),
        name='register'
    ),
    path('', include('django.contrib.auth.urls')),
    path(
        'successfully-created-registration-request/',
        views.successfully_created_registration_request,
        name='successfully_created_registration_request'
    ),
    path('confirm-email/', views.confirm_email, name='confirm_email')
]
