from django.urls import include, path, re_path

import users.views

urlpatterns = [
    re_path(r'^$|home', users.views.index_view),
    re_path(r'users/', include('users.urls')),
    path('administrator/', include('administrator.urls')),
]
