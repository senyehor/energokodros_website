from django.urls import path

from users import views

urlpatterns = [
    path('add-user', views.debug)
]
