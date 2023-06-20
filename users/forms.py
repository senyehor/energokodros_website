from django.contrib.auth import forms as auth_forms


class LoginForm(auth_forms.AuthenticationForm):
    error_messages = {
        'invalid_login': 'Уведіть правильну електронну пошту та пароль'
    }
