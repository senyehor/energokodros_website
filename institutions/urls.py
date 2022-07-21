from django.urls import path

from institutions.views import AccessLevelListView

access_level_patters = [
    path('access-levels/', AccessLevelListView.as_view(), name='access-levels'),
    path('access-levels/new/', lambda x: None, name='access-levels-new'),
]

urlpatterns = access_level_patters
