from datetime import timedelta

from django import forms
from django.contrib.auth.views import LoginView as LogView

from users.forms import LoginForm


class LoginView(LogView):
    form_class = LoginForm
    remember_me = forms.BooleanField(required=False, label="Запам'ятати мене на два тижні")

    def form_valid(self, form):
        if form.data.get('remember_me'):
            self.request.session.set_expiry(timedelta(weeks=2))
        return super().form_valid(form)
