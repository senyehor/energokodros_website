from django.urls import path, include

from users import views

overridden_account_patterns = [
    path('login', views.LoginView.as_view(template_name='registration/login.html')),
]

urlpatterns = [
    include('django.contrib.auth.urls'),

]
