"""
Theater CMS Admin Package

This package contains all Django admin interface components organized into logical modules:
- forms.py: Custom form classes and validation
- widgets.py: Custom form widgets  
- inlines.py: Inline admin classes
- admins.py: Main admin model classes
- backup.py: Backup management admin interface
"""

# Import all components to register them with Django admin
from .forms import *
from .widgets import *
from .inlines import *
from .admins import *
from .backup import *

# The admin registrations happen in the individual modules
