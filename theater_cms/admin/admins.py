"""
Main Admin Classes

This module contains all ModelAdmin classes for the Theater CMS admin interface.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.urls import path, reverse
from theater_cms.models import Event, Performance, SeasonalSponsor, EventSponsorImage, UserFeedback, EmailSubscription, SponsorsPageContent
from .forms import EventForm, SeasonalSponsorForm
from .inlines import EventSponsorImageInline


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model with custom form and inlines"""
    
    form = EventForm
    list_display = ('title', 'composer', 'is_active', 'start_datetime')
    list_filter = ('is_active', 'start_datetime')
    search_fields = ('title', 'composer', 'conductor', 'director')
    inlines = [EventSponsorImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'composer', 'language', 'conductor', 'director')
        }),
        ('Content', {
            'fields': ('cast_content', 'duration', 'about_content')
        }),
        ('Arabic Translations', {
            'fields': ('title_ar', 'composer_ar', 'about_content_ar', 'language_ar', 'conductor_ar', 'director_ar', 'cast_content_ar', 'duration_ar'),
            'classes': ('collapse',)
        }),
        ('General Settings', {
            'fields': ('is_active', 'sort_order'),
            'classes': ('collapse',)
        })
    )
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Override change view to add custom JavaScript for delete confirmation and file input styling"""
        extra_context = extra_context or {}
        
        # Add custom CSS and JavaScript for file inputs and delete confirmation
        extra_context['extra_style'] = mark_safe("""
        <style>
            /* Enhanced file input styling */
            .field-image input[type="file"], 
            .field-image .customfileinput input[type="file"],
            input[type="file"][name*="image"] {
                padding: 8px;
                border: 2px dashed #ccc;
                border-radius: 4px;
                background: #f9f9f9;
                width: 100%;
                box-sizing: border-box;
                transition: border-color 0.3s ease;
            }
            
            .field-image input[type="file"]:hover,
            .field-image .customfileinput input[type="file"]:hover,
            input[type="file"][name*="image"]:hover {
                border-color: #2196f3;
                background: #f0f8ff;
            }
            
            /* Style for inline forms */
            .inline-group input[type="file"] {
                width: auto;
                min-width: 200px;
            }
            
            /* Delete confirmation styling */
            .delete-confirmed {
                background-color: #ffebee !important;
                opacity: 0.7;
                transition: all 0.3s ease;
            }
            
            .delete-warning {
                color: #d32f2f;
                font-weight: bold;
                margin-left: 10px;
            }
            
            /* Event Sponsor Images inline styling - Clean without background */
            #eventsponsorimage_set-group h2 {
                color: #2196F3;
                font-weight: 600;
                font-size: 16px;
                padding: 15px 0 10px 0;
                margin-bottom: 15px;
                border: none;
                background: transparent;
            }
            
            #eventsponsorimage_set-group {
                border: none;
                padding: 0;
            }
            
            #eventsponsorimage_set-group .tabular {
                border-top: 2px solid #e0e0e0;
                padding-top: 15px;
            }
        </style>
        
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Add delete confirmation for inline forms
            function addDeleteConfirmation() {
                var deleteCheckboxes = document.querySelectorAll('input[type="checkbox"][name*="DELETE"]');
                
                deleteCheckboxes.forEach(function(checkbox) {
                    // Avoid double event listeners
                    if (checkbox.hasAttribute('data-delete-listener')) return;
                    checkbox.setAttribute('data-delete-listener', 'true');
                    
                    checkbox.addEventListener('change', function() {
                        if (this.checked) {
                            var confirmDelete = confirm('Are you sure you want to delete this item? This action cannot be undone.');
                            
                            if (confirmDelete) {
                                // Add visual feedback
                                var row = this.closest('tr') || this.closest('.inline-related');
                                if (row) {
                                    row.classList.add('delete-confirmed');
                                    
                                    // Add warning text
                                    var warningSpan = row.querySelector('.delete-warning');
                                    if (!warningSpan) {
                                        warningSpan = document.createElement('span');
                                        warningSpan.className = 'delete-warning';
                                        warningSpan.textContent = '⚠️ Will be deleted';
                                        this.parentNode.appendChild(warningSpan);
                                    }
                                }
                            } else {
                                // User cancelled, uncheck the box
                                this.checked = false;
                            }
                        } else {
                            // Remove visual feedback when unchecked
                            var row = this.closest('tr') || this.closest('.inline-related');
                            if (row) {
                                row.classList.remove('delete-confirmed');
                                var warningSpan = row.querySelector('.delete-warning');
                                if (warningSpan) {
                                    warningSpan.remove();
                                }
                            }
                        }
                    });
                });
            }
            
            // Initial setup
            addDeleteConfirmation();
            
            // Watch for dynamically added inline forms
            if (typeof MutationObserver !== 'undefined') {
                var observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                            // Check if new forms were added
                            var hasNewForms = false;
                            mutation.addedNodes.forEach(function(node) {
                                if (node.nodeType === 1 && (
                                    node.classList.contains('inline-related') || 
                                    node.querySelector && node.querySelector('.inline-related')
                                )) {
                                    hasNewForms = true;
                                }
                            });
                            
                            if (hasNewForms) {
                                setTimeout(addDeleteConfirmation, 100);
                            }
                        }
                    });
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
            }
        });
        </script>
        """)
        
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    """
    Unified Performance Scheduling Admin - Calendar-style interface
    Schedule multiple performances of different events on the same day
    """
    
    list_display = ('calendar_date', 'time_slot', 'event_display', 'quick_actions')
    list_filter = ('event', 'start_time')
    search_fields = ('event__title', 'event__title_ar')
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)
    
    # Use custom calendar-style template
    change_list_template = 'admin/theater_cms/performance/change_list.html'
    
    fieldsets = (
        ('Event Selection', {
            'fields': ('event',),
            'description': 'Select which event/show this performance is for (e.g., Rigoletto, Aida, etc.)'
        }),
        ('Performance Schedule', {
            'fields': ('start_time', 'end_time'),
            'description': 'Set the exact date and time for this specific performance'
        }),
    )
    
    # Custom list display methods
    def calendar_date(self, obj):
        """Display date in a calendar-friendly format"""
        if not obj.start_time:
            return format_html('<span style="color: #999;">No date set</span>')
        
        date_str = obj.start_time.strftime('%A, %B %d, %Y')
        day_num = obj.start_time.strftime('%d')
        month_abbr = obj.start_time.strftime('%b')
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 12px;">'
            '<div style="background: #2196F3; color: white; padding: 8px 12px; '
            'border-radius: 6px; text-align: center; min-width: 60px; font-weight: bold;">'
            '<div style="font-size: 10px; opacity: 0.9;">{}</div>'
            '<div style="font-size: 18px;">{}</div>'
            '</div>'
            '<div style="color: #555; font-weight: 500;">{}</div>'
            '</div>',
            month_abbr.upper(),
            day_num,
            date_str.split(',')[0]  # Day of week
        )
    calendar_date.short_description = 'Date'
    calendar_date.admin_order_field = 'start_time'
    
    def time_slot(self, obj):
        """Display time slot clearly"""
        if not obj.start_time:
            return format_html('<span style="color: #999;">No time set</span>')
        
        start_str = obj.start_time.strftime('%I:%M %p')
        
        if obj.end_time:
            end_str = obj.end_time.strftime('%I:%M %p')
            duration = obj.end_time - obj.start_time
            hours = duration.total_seconds() / 3600
            duration_text = f"{round(hours, 1)}h"
        else:
            end_str = "~3h later"
            duration_text = "~3h"
        
        return format_html(
            '<div style="line-height: 1.8;">'
            '<div><strong style="color: #2196F3; font-size: 15px;">🕐 {} - {}</strong></div>'
            '<div style="color: #666; font-size: 12px;">Duration: {}</div>'
            '</div>',
            start_str,
            end_str if obj.end_time else end_str,
            duration_text
        )
    time_slot.short_description = 'Time Slot'
    
    def event_display(self, obj):
        """Display event with visual indicator"""
        if not obj.event:
            return format_html('<span style="color: #999;">No event</span>')
        
        # Generate a consistent color based on event title
        color_map = {
            'A': '#E91E63', 'B': '#9C27B0', 'C': '#673AB7', 'D': '#3F51B5',
            'E': '#2196F3', 'F': '#00BCD4', 'G': '#009688', 'H': '#4CAF50',
            'I': '#8BC34A', 'J': '#CDDC39', 'K': '#FFC107', 'L': '#FF9800',
            'M': '#FF5722', 'N': '#795548', 'O': '#607D8B', 'P': '#E91E63',
            'Q': '#9C27B0', 'R': '#673AB7', 'S': '#3F51B5', 'T': '#2196F3',
            'U': '#00BCD4', 'V': '#009688', 'W': '#4CAF50', 'X': '#8BC34A',
            'Y': '#CDDC39', 'Z': '#FFC107'
        }
        
        first_char = obj.event.title[0].upper() if obj.event.title else 'A'
        color = color_map.get(first_char, '#2196F3')
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<div style="width: 12px; height: 12px; background: {}; '
            'border-radius: 50%; flex-shrink: 0;"></div>'
            '<span style="font-weight: 600; color: {};">🎭 {}</span>'
            '</div>',
            color,
            color,
            obj.event.title
        )
    event_display.short_description = 'Event'
    event_display.admin_order_field = 'event'
    
    def quick_actions(self, obj):
        """Quick action buttons for common operations"""
        duplicate_url = reverse('admin:theater_cms_performance_add') + f'?event={obj.event.id}'
        
        return format_html(
            '<div style="display: flex; gap: 8px;">'
            '<a class="button" href="{}" '
            'style="background: #4CAF50; color: white; padding: 6px 12px; '
            'border-radius: 4px; text-decoration: none; font-size: 11px; white-space: nowrap;">'
            '➕ Duplicate</a>'
            '</div>',
            duplicate_url
        )
    quick_actions.short_description = 'Actions'
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Customize the add/edit form view"""
        extra_context = extra_context or {}
        extra_context['title'] = 'Schedule Performance'
        
        extra_context['extra_style'] = mark_safe("""
        <style>
            /* Event selection styling */
            .form-row.field-event {
                background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 25px;
                border-left: 4px solid #2196F3;
            }
            
            .form-row.field-event label {
                color: #1565C0;
                font-weight: 700;
                font-size: 16px;
                margin-bottom: 10px;
                display: block;
            }
            
            .form-row.field-event label::before {
                content: "🎭 ";
                font-size: 18px;
                margin-right: 8px;
            }
            
            .form-row.field-event select {
                width: 100%;
                max-width: 500px;
                padding: 12px 15px;
                font-size: 15px;
                border: 2px solid #2196F3;
                border-radius: 6px;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .form-row.field-event select:focus {
                outline: none;
                border-color: #1565C0;
                box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
            }
            
            /* Time fields styling */
            .form-row.field-start_time,
            .form-row.field-end_time {
                background: #F5F5F5;
                padding: 18px;
                border-radius: 8px;
                margin: 12px 0;
                border-left: 4px solid #2196F3;
            }
            
            .form-row.field-start_time label,
            .form-row.field-end_time label {
                color: #2196F3;
                font-weight: 600;
                font-size: 15px;
                display: block;
                margin-bottom: 8px;
            }
            
            .form-row.field-start_time label::before {
                content: "🗓️ ";
                font-size: 18px;
                margin-right: 8px;
            }
            
            .form-row.field-end_time label::before {
                content: "🏁 ";
                font-size: 18px;
                margin-right: 8px;
            }
            
            .form-row.field-start_time input,
            .form-row.field-end_time input {
                padding: 10px 12px;
                font-size: 14px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                width: 100%;
                max-width: 350px;
                background: white;
            }
            
            .form-row.field-start_time input:focus,
            .form-row.field-end_time input:focus {
                border-color: #2196F3;
                outline: none;
                box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
            }
            
            /* Help text styling */
            .form-row .help {
                color: #666;
                font-size: 13px;
                margin-top: 6px;
                font-style: italic;
            }
        </style>
        """)
        
        return super().change_view(request, object_id, form_url, extra_context)
    
    def add_view(self, request, form_url='', extra_context=None):
        """Customize the add form view"""
        extra_context = extra_context or {}
        extra_context['title'] = 'Schedule New Performance'
        return super().add_view(request, form_url, extra_context)
    
    def changelist_view(self, request, extra_context=None):
        """Enhanced calendar-style list view"""
        extra_context = extra_context or {}
        extra_context['title'] = 'Performance Calendar'
        
        extra_context['extra_style'] = mark_safe("""
        <style>
            /* Header styling */
            #changelist h1 {
                color: #1565C0;
                font-size: 28px;
                margin-bottom: 20px;
            }
            
            #changelist h1::before {
                content: "📅 ";
                font-size: 32px;
                margin-right: 10px;
            }
            
            /* Table header styling */
            #result_list thead th {
                background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
                color: white;
                font-weight: 600;
                padding: 14px 10px;
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 0.5px;
            }
            
            /* Table row styling */
            #result_list tbody tr {
                transition: all 0.2s ease;
            }
            
            #result_list tbody tr:hover {
                background: #E3F2FD;
                transform: scale(1.01);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            #result_list tbody td {
                padding: 12px 10px;
                vertical-align: middle;
            }
            
            /* Add button styling */
            .addlink {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
                color: white !important;
                padding: 10px 20px !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                text-decoration: none !important;
                display: inline-block !important;
                margin-bottom: 20px !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
                transition: all 0.2s ease !important;
            }
            
            .addlink:hover {
                background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%) !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
                transform: translateY(-2px) !important;
            }
            
            .addlink::before {
                content: "➕ ";
                font-size: 14px;
                margin-right: 6px;
            }
            
            /* Filter sidebar styling */
            #changelist-filter {
                background: #F5F5F5;
                border-left: 3px solid #2196F3;
            }
            
            #changelist-filter h2 {
                background: #2196F3;
                color: white;
                padding: 10px;
                font-size: 14px;
            }
            
            #changelist-filter h3 {
                color: #1565C0;
                font-weight: 600;
            }
            
            /* Search bar */
            #searchbar {
                border: 2px solid #2196F3;
                border-radius: 4px;
                padding: 8px 12px;
            }
            
            #searchbar:focus {
                outline: none;
                box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
            }
        </style>
        """)
        
        return super().changelist_view(request, extra_context)


@admin.register(SeasonalSponsor)
class SeasonalSponsorAdmin(admin.ModelAdmin):
    """Admin interface for SeasonalSponsor model with image validation"""
    
    form = SeasonalSponsorForm
    list_display = ('name', 'image_status')
    search_fields = ('name',)
    ordering = ('name',)
    
    def image_status(self, obj):
        """Display image status in list view"""
        if obj.image:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Has Image</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ No Image</span>'
            )
    image_status.short_description = 'Image Status'


@admin.register(EventSponsorImage)
class EventSponsorImageAdmin(admin.ModelAdmin):
    """Admin interface for EventSponsorImage model"""
    
    list_display = ('name', 'event', 'image_preview')
    list_filter = ('event',)
    search_fields = ('name', 'event__title')
    ordering = ('name',)
    
    def image_preview(self, obj):
        """Display small image preview in list view"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    """Simple admin for UserFeedback model"""
    list_display = ('name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'comments')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    """Simple admin for EmailSubscription model"""
    list_display = ('email', 'name', 'receive_updates', 'subscribed_at')
    list_filter = ('receive_updates', 'subscribed_at')
    search_fields = ('email', 'name')
    readonly_fields = ('subscribed_at',)
    ordering = ('-subscribed_at',)


@admin.register(SponsorsPageContent)
class SponsorsPageContentAdmin(admin.ModelAdmin):
    """Simple admin for SponsorsPageContent model"""
    list_display = ('sponsors_title_en', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('sponsors_title_en', 'sponsors_intro_en', 'sponsors_title_ar', 'sponsors_intro_ar')
    ordering = ('-updated_at',)
    
    fieldsets = (
        ('English Content', {
            'fields': ('sponsors_title_en', 'sponsors_intro_en')
        }),
        ('Arabic Content', {
            'fields': ('sponsors_title_ar', 'sponsors_intro_ar')
        })
    )
    
    readonly_fields = ('updated_at',)
