from django.urls import include, path, re_path, register_converter

from users.views import index_view
from utils.crypto import IntHasher, StringHasher

register_converter(IntHasher, 'hashed_int')
register_converter(StringHasher, 'hashed_str')

urlpatterns = [
    re_path(r'^$|home', index_view, name='home'),
    path('users/', include('users.urls')),
    path('administrator/', include('administrator.urls')),
]
