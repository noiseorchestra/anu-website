from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'dashboard'

urlpatterns = [
    path('recordings/', views.recordings_list),
    path('recordings/<path:file>', views.get_download_link),
    path('<slug:slug>/', views.dashboard, name='dashboard'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
