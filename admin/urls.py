from django.urls import path

from admin import views

urlpatterns = [
    path(
        'admin-page',
        views.admin_page,
        name='admin_page'
    ),
    path(
        'review-registration-request',
        views.RegistrationRequestReview.as_view(),
        name='review_registration_request'
    ),
    path(
        'get-message-for-registration-request',
        views.GetMessageForRegistrationRequest.as_view(),
        name='get_message_for_registration_request_link'
    )
]
