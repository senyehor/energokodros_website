from django.urls import include, path, re_path, register_converter

import users.views
from utils.crypto import IntHasher, StringHasher

register_converter(IntHasher, 'hashed_int')
register_converter(StringHasher, 'hashed_str')

urlpatterns = [
    re_path(r'^$|home', users.views.index_view, name='home'),
    path('users/', include('users.urls')),
    path('administrator/', include('administrator.urls')),
]
