from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theater_cms.urls')),  # Include your app's URLs at root level
]

# Translated URLs
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),  # Keep the CMS URLs last
)

# Fix: Remove the manual static configuration - Django handles this automatically when DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Django automatically serves static files when DEBUG=True, no need to add static URL patterns