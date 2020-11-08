from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('recordings/', views.recordings_list),
    path('<slug:slug>/', views.dashboard, name='dashboard'),
]
