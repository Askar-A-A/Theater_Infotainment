from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # Keep this for non-i18n URLs if needed
    # path('', include('theater_cms.urls')),
]

# Translated URLs - removed CMS URLs and using our theater_cms URLs instead
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('theater_cms.urls')),  # Replace CMS URLs with our app's URLs
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)