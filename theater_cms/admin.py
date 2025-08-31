"""
Theater CMS Admin Configuration

This module imports and registers all admin components from the restructured admin package.
The actual admin implementations are now organized in separate modules:
- admin/forms.py: Custom form classes and validation
- admin/widgets.py: Custom form widgets
- admin/inlines.py: Inline admin classes
- admin/admins.py: Main admin model classes
- admin/backup.py: Backup management admin interface
- services/: Business logic and utility functions
"""

from django.contrib import admin
from .models import Event, Performance, UserFeedback, EmailSubscription, SeasonalSponsor, EventSponsorImage, SponsorsPageContent

# Import all admin components - this registers all the admin classes
from .admin import *

# The admin registrations and configurations are handled in the imported modules:
# - EventAdmin, PerformanceAdmin, SeasonalSponsorAdmin, EventSponsorImageAdmin are in admin/admins.py
# - Backup functionality is in admin/backup.py
# - Forms and widgets are in their respective modules
# - Services are in the services/ package

# All admin registrations are now handled in the imported admin modules:
# - EventAdmin, PerformanceAdmin, SeasonalSponsorAdmin, EventSponsorImageAdmin are in admin/admins.py
# - UserFeedbackAdmin, EmailSubscriptionAdmin, SponsorsPageContentAdmin are in admin/admins.py
# - Backup functionality is in admin/backup.py 