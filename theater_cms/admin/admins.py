"""
Main Admin Classes

This module contains all ModelAdmin classes for the Theater CMS admin interface.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from theater_cms.models import Event, Performance, SeasonalSponsor, EventSponsorImage, UserFeedback, EmailSubscription, SponsorsPageContent
from .forms import EventForm, SeasonalSponsorForm
from .inlines import PerformanceInline, EventSponsorImageInline


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model with custom form and inlines"""
    
    form = EventForm
    list_display = ('title', 'composer', 'is_active', 'start_datetime')
    list_filter = ('is_active', 'start_datetime')
    search_fields = ('title', 'composer', 'conductor', 'director')
    inlines = [PerformanceInline, EventSponsorImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'composer', 'language', 'conductor', 'director')
        }),
        ('Content', {
            'fields': ('cast_content', 'duration', 'about_content')
        }),
        ('Dates & Settings', {
            'fields': ('is_active', 'sort_order', 'start_datetime', 'end_datetime'),
            'classes': ('collapse',)
        }),
        ('Arabic Translations', {
            'fields': ('title_ar', 'composer_ar', 'about_content_ar', 'language_ar', 'conductor_ar', 'director_ar', 'cast_content_ar', 'duration_ar'),
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
    """Admin interface for Performance model"""
    
    list_display = ('event', 'start_time', 'end_time')
    list_filter = ('start_time', 'event')
    search_fields = ('event__title',)
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)


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
