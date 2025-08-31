"""
User Management Service

This module handles user and group management operations for the Theater CMS.
Provides functions for setting up admin groups and permissions.
"""

from django.contrib.auth.models import Group, Permission
from django.db.models import Q


def setup_admin_groups():
    """Create a function to set up admin groups"""
    # Create or get the content editor group
    content_editors, created = Group.objects.get_or_create(name='Content Editors')
    
    # Clear existing permissions if the group already exists
    if not created:
        content_editors.permissions.clear()
    
    # Add specific permissions for content management
    # Get all permissions for models that content editors should manage
    content_permissions = Permission.objects.filter(
        Q(content_type__app_label='theater_cms') & 
        (Q(content_type__model='event') | 
         Q(content_type__model='performance') |
         Q(content_type__model='seasonalsponsor') |
         Q(content_type__model='eventsponsorimage'))
    )
    
    # Add these permissions to the group
    content_editors.permissions.add(*content_permissions)
