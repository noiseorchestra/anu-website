from django.contrib import admin
from django.urls import path, include, url

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('django.contrib.auth.urls')),

    # File uploads
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # Local apps
    path('', include('pages.urls')),
]
