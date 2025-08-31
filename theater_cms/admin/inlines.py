"""
Admin Inline Classes

This module contains all inline admin classes for the Theater CMS admin interface.
"""

from django.contrib import admin
from theater_cms.models import Performance, EventSponsorImage
from .forms import EventSponsorImageForm


class PerformanceInline(admin.TabularInline):
    """Inline admin for Performance model"""
    model = Performance
    extra = 1
    fields = ('start_time', 'end_time')


class EventSponsorImageInline(admin.TabularInline):
    """Inline admin for EventSponsorImage model with custom form"""
    model = EventSponsorImage
    form = EventSponsorImageForm
    extra = 1
    fields = ('name', 'image')
    
    def get_formset(self, request, obj=None, **kwargs):
        """Customize the formset for inline sponsor images"""
        formset = super().get_formset(request, obj, **kwargs)
        formset.form = EventSponsorImageForm
        return formset
