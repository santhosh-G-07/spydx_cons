from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ only one admin route!
    path('api/', include('consultant_api.urls')),  # ✅ for API endpoints
    path('', include('consultant_api.urls')),      # ✅ for frontend views
]

# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
