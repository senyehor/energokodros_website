from django.urls import include, path, re_path, register_converter, reverse_lazy
from django.views.generic import RedirectView

from utils.crypto import IntHasher, StringHasher

register_converter(IntHasher, 'hashed_int')
register_converter(StringHasher, 'hashed_str')

urlpatterns = [
    re_path(
        r'^$|home',
        RedirectView.as_view(url=reverse_lazy('aggregated-consumption')),
        name='home'
    ),
    path('users/', include('users.urls')),
    path('administrator/', include('administrator.urls')),
    path('energy/', include('energy.urls'))
]
