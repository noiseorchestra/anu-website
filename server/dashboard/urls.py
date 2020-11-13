from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from modernrpc.views import RPCEntryPoint

app_name = 'dashboard'

urlpatterns = [
    path('recordings/', views.recordings_list),
    path('recordings/<path:file>', views.get_download_link),
    re_path(r'^rpc/', RPCEntryPoint.as_view(enable_doc=True)),
    path('<slug:slug>/', views.dashboard, name='dashboard'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
