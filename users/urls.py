from django.urls import path, include

from users import views

overridden_account_patterns = [
    path('login', views.LoginView.as_view(template_name='registration/login.html')),
]

urlpatterns = overridden_account_patterns + [
    path('registration', views.CreateUserRegistrationRequest.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path(
        'successfully-created-registration-request',
        views.successfully_created_registration_request,
        name='successfully_created_registration_request'
    ),

]
