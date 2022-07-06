from django.urls import path

from administrator import views

urlpatterns = [
    path(
        '',
        views.admin_page,
        name='admin_page'
    ),
    path(
        'review-registration-request/',
        views.review_registration_request,
        name='review_registration_request'
    ),
    path(
        'get-message-for-registration-request/',
        views.get_message_for_registration_request,
        name='get_message_for_registration_request'
    )
]
