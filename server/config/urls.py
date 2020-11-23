from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('django.contrib.auth.urls')),

    # File uploads
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Local apps
    path('dashboard/', include('dashboard.urls')),
    path('sounds/', include('sounds.urls')),
    path('', include('pages.urls')),
]
