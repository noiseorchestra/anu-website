from django.urls import path
from .views import HomePageView
from . import views

urlpatterns = [
    path('<slug:slug>/', views.page, name='page'),
    path('', HomePageView.as_view(), name='home'),
]
