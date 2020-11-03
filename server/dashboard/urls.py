from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.vue_naw_dashboard, name='dashboard'),
]
