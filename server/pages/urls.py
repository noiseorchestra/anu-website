from django.urls import path
from .views import HomePageView
from . import views

app_name = 'pages'

urlpatterns = [
    path('<slug:slug>/', views.page, name='page'),
    path('', views.page, name='home'),
]
