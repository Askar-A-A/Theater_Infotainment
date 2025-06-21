from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theater_cms.urls')),  # Include your app's URLs at root level
    path('', include('cms.urls')),  # CMS URLs - moved outside i18n_patterns
]

# Remove the i18n_patterns section since you're not using Django's i18n system
# urlpatterns += i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('', include('cms.urls')),  # Keep the CMS URLs last
# )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)