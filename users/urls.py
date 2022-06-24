from django.urls import path, include, re_path

from users import views

# using /? to override some of django.contrib.auth.urls
overridden_account_patterns = [
    re_path('login/?', views.LoginView.as_view(template_name='registration/login.html')),
]

urlpatterns = overridden_account_patterns + [
    re_path('registration/?', views.CreateUserRegistrationRequest.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path(
        'successfully-created-registration-request',
        views.successfully_created_registration_request,
        name='successfully_created_registration_request'
    ),
    path(
        'review-registration-request',
        views.RegistrationRequestReview.as_view(),
        name='review_registration_request'
    ),
    path(
        'admin-page',
        views.admin_page,
        name='admin_page'
    ),
    path(
        'get-message-for-registration-request',
        views.GetMessageForRegistrationRequest.as_view(),
        name='get_message_for_registration_request_link'
    )
]
