from django.contrib import admin
from django import forms
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import Event, Performance, UserFeedback, EmailSubscription, SeasonalSponsor, EventSponsorImage, SponsorsPageContent
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models import Q

# Create a function to set up admin groups
def setup_admin_groups():
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

# Call this function when Django loads (in apps.py or in a migration)

# Custom forms for sponsor validation
class SeasonalSponsorForm(forms.ModelForm):
    class Meta:
        model = SeasonalSponsor
        fields = '__all__'
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("An image is required for all sponsors. Please upload a sponsor logo.")
        return image

class EventSponsorImageForm(forms.ModelForm):
    class Meta:
        model = EventSponsorImage
        fields = '__all__'
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("An image is required for all sponsors. Please upload a sponsor logo.")
        return image

class PerformanceInline(admin.TabularInline):
    model = Performance
    extra = 0  # Show no empty forms by default, use bulk scheduler instead
    fields = ('performance_date', 'performance_time', 'end_time')
    readonly_fields = ('end_time',)  # Make end_time read-only since it's auto-calculated
    
    # Use custom formfield overrides for better date/time inputs
    formfield_overrides = {
        models.DateTimeField: {'widget': admin.widgets.AdminSplitDateTime},
    }
    
    # Add these methods to split datetime into date and time
    def performance_date(self, obj):
        if obj and obj.start_time:
            return obj.start_time.date()
        return None
    performance_date.short_description = "Date"
    
    def performance_time(self, obj):
        if obj and obj.start_time:
            return obj.start_time.time()
        return None
    performance_time.short_description = "Time"
    
    # We need to provide a custom formset to handle the date/time split
    def get_formset(self, request, obj=None, **kwargs):
        from django import forms
        from datetime import datetime, timedelta
        
        # Create a custom form for the inline
        class PerformanceForm(forms.ModelForm):
            # Add separate date and time fields
            performance_date = forms.DateField(
                label="Date",
                widget=forms.DateInput(attrs={'type': 'date'}),
                required=False,  # Make it not required for existing performances
            )
            performance_time = forms.TimeField(
                label="Time",
                widget=forms.TimeInput(attrs={'type': 'time'}),
                initial='19:30',
                required=False,  # Make it not required for existing performances
            )
            
            class Meta:
                model = Performance
                fields = ['performance_date', 'performance_time']
                
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Pre-populate date and time fields if we have an existing instance
                if self.instance and self.instance.pk and self.instance.start_time:
                    self.fields['performance_date'].initial = self.instance.start_time.date()
                    self.fields['performance_time'].initial = self.instance.start_time.time()
                    
                    # Add a hidden field to store the original start_time
                    self.fields['original_start_time'] = forms.CharField(
                        widget=forms.HiddenInput(),
                        required=False,
                        initial=self.instance.start_time.isoformat()
                    )
            
            def clean(self):
                cleaned_data = super().clean()
                # If the form is for an existing performance and the date/time fields are empty,
                # keep the original start_time
                if self.instance and self.instance.pk and not cleaned_data.get('performance_date'):
                    # Re-use the original start_time
                    return cleaned_data
                
                # Ensure both date and time are provided for new entries
                if not self.instance.pk and (not cleaned_data.get('performance_date') or not cleaned_data.get('performance_time')):
                    raise forms.ValidationError("Both date and time are required for new performances")
                
                return cleaned_data
            
            def save(self, commit=True):
                # Don't call save yet
                instance = super().save(commit=False)
                
                # Only update the datetime if both date and time are provided
                date = self.cleaned_data.get('performance_date')
                time = self.cleaned_data.get('performance_time')
                
                if date and time:
                    # Combine date and time into datetime
                    instance.start_time = datetime.combine(date, time)
                    
                    # Set end time based on duration
                    duration = instance.event.standard_duration or timedelta(hours=3)
                    instance.end_time = instance.start_time + duration
                
                if commit:
                    instance.save()
                
                return instance
                
        # Create a custom formset that uses our custom form
        class CustomInlineFormSet(forms.models.BaseInlineFormSet):
            form = PerformanceForm
            
            def save_new(self, form, commit=True):
                # Handle saving new forms
                return form.save(commit=commit)
            
            def save_existing(self, form, instance, commit=True):
                # Handle saving existing forms 
                return form.save(commit=commit)
        
        # Return the formset with our customizations
        defaults = {
            "formset": CustomInlineFormSet,
            "form": PerformanceForm,
        }
        defaults.update(kwargs)
        return super().get_formset(request, obj, **defaults)

class EventSponsorImageInline(admin.TabularInline):
    model = EventSponsorImage
    form = EventSponsorImageForm  # Use our custom form with validation
    extra = 1  # Show one empty form by default
    fields = ('name', 'image')  # website removed from fields

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_zh_short', 'composer', 'date_range_display', 'performance_count', 'is_active', 'schedule_button')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active',)
    search_fields = ('title', 'composer', 'title_zh', 'composer_zh')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'composer', 'image', 'is_active', 'sort_order')
        }),
        ('Chinese Translation', {
            'fields': ('title_zh', 'composer_zh'),
            'classes': ('collapse',),
            'description': 'Chinese translations for basic information'
        }),
        ('Duration Information', {
            'fields': ('standard_duration', 'duration', 'duration_zh'),
            'description': 'Standard duration is used to automatically calculate end times when scheduling performances.'
        }),
        ('Content Details (English)', {
            'fields': ('about_content', 'language', 'conductor', 'director', 'cast_content', 'additional_details'),
            'classes': ('collapse',),
        }),
        ('Content Details (Chinese)', {
            'fields': ('about_content_zh', 'language_zh', 'conductor_zh', 'director_zh', 'cast_content_zh'),
            'classes': ('collapse',),
            'description': 'Chinese translations for detailed content'
        }),
    )
    inlines = [PerformanceInline, EventSponsorImageInline]
    
    def title_zh_short(self, obj):
        """Show shortened Chinese title in list view"""
        if obj.title_zh:
            return obj.title_zh[:30] + "..." if len(obj.title_zh) > 30 else obj.title_zh
        return "-"
    title_zh_short.short_description = 'Chinese Title'
    
    # Add a field for the help text above the inline
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        
        # Add more descriptive help text with formatting
        extra_context['performance_help_text'] = (
            "Use 'Schedule Performances' for adding multiple performances more easily. "
            "The section below is for manual adjustments to individual performances."
        )
        
        # Add custom CSS for the performances section
        extra_context['extra_style'] = """
        <style>
            /* Improved performance section */
            #performance-section {
                margin-top: 20px;
                padding: 15px 20px;
                background-color: #f9f9f9;
                border-radius: 4px;
                border-left: 4px solid #79aec8;
            }
            
            #performance-section h2 {
                margin-top: 0;
                color: #417690;
                font-size: 16px;
                margin-bottom: 10px;
            }
            
            #performance-section p {
                margin-bottom: 15px;
                color: #666;
            }
            
            /* Better styling for the bulk scheduling button */
            .schedule-btn {
                display: inline-block;
                background-color: #417690;
                color: white !important;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                text-decoration: none !important;
                transition: background-color 0.2s;
                margin-bottom: 15px;
            }
            
            .schedule-btn:hover {
                background-color: #295a70;
            }
            
            /* Improve the inline formset appearance */
            .tabular.inline-related {
                margin-top: 0;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                overflow: hidden;
                background-color: #fff;
            }
            
            /* Remove the rectangular border around "Performances" */
            .tabular.inline-related h2 {
                display: none; /* Hide the default header */
            }
            
            .tabular.inline-related .tabular {
                border: none !important;
            }
            
            /* Make the inline headers more pleasant */
            .tabular.inline-related .module h3 {
                background-color: #f1f1f1;
                padding: 10px 15px;
                margin: 0;
                border-bottom: 1px solid #e0e0e0;
                font-size: 14px;
            }
            
            /* Better styling for the form rows */
            .tabular.inline-related .form-row {
                padding: 12px 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .tabular.inline-related .form-row:last-child {
                border-bottom: none;
            }
            
            /* Improve field styling */
            .performance-field {
                display: inline-block;
                margin-right: 15px;
            }
            
            /* Make the notes field bigger */
            .field-notes input {
                width: 300px !important;
            }
            
            /* Fix spacing for the add another row */
            .add-row {
                padding: 10px 15px !important;
                background-color: #f8f8f8 !important;
            }
            
            /* Table headers for the performances */
            .tabular.inline-related .module thead th {
                background-color: #eaeaea;
                padding: 8px 15px;
            }
        </style>
        """
        
        # Use a better URL for bulk scheduling
        if object_id:
            event = self.get_object(request, object_id)
            if event:
                schedule_url = reverse('admin:theater_cms_event_schedule', args=[event.pk])
                extra_context['schedule_url'] = schedule_url
                
        return super().change_view(request, object_id, form_url, extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:event_id>/schedule/',
                self.admin_site.admin_view(self.bulk_schedule_view),
                name='theater_cms_event_schedule'),
        ]
        return custom_urls + urls
    
    def performance_count(self, obj):
        count = obj.performances.count()
        return format_html(
            '<a href="{}?event__id__exact={}">{} performances</a>',
            reverse('admin:theater_cms_performance_changelist'),
            obj.id,
            count
        )
    performance_count.short_description = 'Performances'
    
    def schedule_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Schedule Performances</a>',
            reverse('admin:theater_cms_event_schedule', args=[obj.pk])
        )
    schedule_button.short_description = 'Schedule'
    
    def bulk_schedule_view(self, request, event_id):
        """View for bulk scheduling multiple performances"""
        event = Event.objects.get(id=event_id)
        
        class BulkScheduleForm(forms.Form):
            REPEAT_CHOICES = [
                ('single', 'Single Performance'),
                ('weekly', 'Weekly Performances'),
                ('custom', 'Multiple Specific Dates')
            ]
            WEEKDAYS = [
                ('0', 'Monday'),
                ('1', 'Tuesday'),
                ('2', 'Wednesday'),
                ('3', 'Thursday'),
                ('4', 'Friday'),
                ('5', 'Saturday'),
                ('6', 'Sunday'),
            ]

            repeat_type = forms.ChoiceField(
                choices=REPEAT_CHOICES, 
                widget=forms.RadioSelect,
                initial='single',
                label="Scheduling Type"
            )

            # Single Performance Fields
            single_date = forms.DateField(
                widget=forms.DateInput(attrs={'type': 'date'}),
                label="Performance Date",
                help_text="Date for this performance",
                required=False
            )
            single_time = forms.TimeField(
                widget=forms.TimeInput(attrs={'type': 'time'}),
                initial='19:30',
                label="Performance Time",
                help_text="Start time (e.g., 19:30)",
                required=False
            )

            # New Weekly Performance Fields
            weekly_start_date = forms.DateField(
                widget=forms.DateInput(attrs={'type': 'date'}),
                label="Start Date",
                help_text="Date to start scheduling performances",
                required=False
            )
            weekly_time = forms.TimeField(
                widget=forms.TimeInput(attrs={'type': 'time'}),
                initial='19:30',
                label="Performance Time",
                help_text="Start time for all performances",
                required=False
            )
            weekly_weekdays = forms.MultipleChoiceField(
                choices=WEEKDAYS,
                widget=forms.CheckboxSelectMultiple,
                label="Days of the Week",
                required=False,
                help_text="Select one or more days for weekly performances",
            )
            weekly_num_weeks = forms.IntegerField(
                label="Number of Weeks",
                min_value=1,
                initial=4,
                required=False,
                help_text="How many weeks to repeat the schedule"
            )

            # Custom Dates Field
            custom_dates = forms.CharField(
                widget=forms.Textarea(attrs={
                    'rows': 5,
                    'placeholder': '2025-04-26 19:30\n2025-04-29 20:00\n2025-04-31 14:00'
                }),
                label="Performance Dates and Times. Copy the Example 2025-01-05 19:30",
                help_text="Enter each performance on a new line as: YYYY-MM-DD HH:MM",
                required=False
            )

            # Common Fields
            duration = forms.DurationField(
                required=False,
                label="Performance Duration",
                help_text="Duration in hours:minutes (e.g., 2:30). Leave blank to use event's standard duration."
            )

            def clean(self):
                cleaned_data = super().clean()
                repeat_type = cleaned_data.get('repeat_type')

                if repeat_type == 'single':
                    if not cleaned_data.get('single_date'):
                        self.add_error('single_date', "Required for single performance")
                    if not cleaned_data.get('single_time'):
                        self.add_error('single_time', "Required for single performance")

                elif repeat_type == 'weekly':
                    if not cleaned_data.get('weekly_start_date'):
                        self.add_error('weekly_start_date', "Required for weekly performances")
                    if not cleaned_data.get('weekly_time'):
                        self.add_error('weekly_time', "Required for weekly performances")
                    if not cleaned_data.get('weekly_weekdays'):
                        self.add_error('weekly_weekdays', "Select at least one weekday")
                    if not cleaned_data.get('weekly_num_weeks'):
                        self.add_error('weekly_num_weeks', "Specify how many weeks to repeat")

                elif repeat_type == 'custom':
                    if not cleaned_data.get('custom_dates'):
                        self.add_error('custom_dates', "Please enter at least one date")

                return cleaned_data

        if request.method == 'POST':
            form = BulkScheduleForm(request.POST)
            if form.is_valid():
                from datetime import datetime, timedelta

                repeat_type = form.cleaned_data['repeat_type']
                duration = form.cleaned_data['duration'] or timedelta(hours=3)

                performances_to_create = []

                if repeat_type == 'single':
                    date = form.cleaned_data['single_date']
                    time = form.cleaned_data['single_time']
                    start_time = datetime.combine(date, time)
                    performances_to_create.append({
                        'start_time': start_time,
                        'end_time': start_time + duration,
                    })

                elif repeat_type == 'weekly':
                    start_date = form.cleaned_data['weekly_start_date']
                    time = form.cleaned_data['weekly_time']
                    weekdays = [int(day) for day in form.cleaned_data['weekly_weekdays']]
                    num_weeks = form.cleaned_data['weekly_num_weeks']

                    # For each week, schedule on each selected weekday
                    for week in range(num_weeks):
                        for weekday in weekdays:
                            # Find the date for this weekday in the current week
                            # Calculate the date for the current week and weekday
                            # start_date.weekday() gives the weekday of the start_date (0=Monday)
                            days_ahead = (weekday - start_date.weekday() + 7) % 7 + week * 7
                            perf_date = start_date + timedelta(days=days_ahead)
                            # Only schedule if this date is not before the start_date
                            if perf_date >= start_date:
                                start_time = datetime.combine(perf_date, time)
                                performances_to_create.append({
                                    'start_time': start_time,
                                    'end_time': start_time + duration,
                                })

                elif repeat_type == 'custom':
                    custom_dates_text = form.cleaned_data['custom_dates']
                    for line in custom_dates_text.split('\n'):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            custom_datetime = datetime.strptime(line, '%Y-%m-%d %H:%M')
                            performances_to_create.append({
                                'start_time': custom_datetime,
                                'end_time': custom_datetime + duration,
                            })
                        except ValueError:
                            continue

                for perf_data in performances_to_create:
                    Performance.objects.create(
                        event=event,
                        start_time=perf_data['start_time'],
                        end_time=perf_data['end_time'],
                    )

                event.update_date_range()

                self.message_user(
                    request, 
                    f"Successfully scheduled {len(performances_to_create)} performances."
                )
                return HttpResponseRedirect(
                    reverse('admin:theater_cms_event_change', args=[event_id])
                )
        else:
            initial = {}
            if event.standard_duration:
                initial['duration'] = event.standard_duration
            form = BulkScheduleForm(initial=initial)

        context = {
            'form': form,
            'event': event,
            'opts': self.model._meta,
            'title': f'Schedule Performances: {event.title}'
        }
        return render(request, 'admin/theater_cms/event/bulk_schedule.html', context)

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('event', 'start_time', 'end_time')
    list_filter = ('event', 'start_time')
    search_fields = ('event__title',)
    date_hierarchy = 'start_time'

@admin.register(SeasonalSponsor)
class SeasonalSponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_status')
    form = SeasonalSponsorForm  # Use our custom form with validation
    
    def image_status(self, obj):
        """Show whether sponsor has an image"""
        if obj.image:
            return format_html('<span style="color: green;">✓ Has Image</span>')
        return format_html('<span style="color: red;">✗ Missing Image</span>')
    image_status.short_description = 'Image Status'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('page-content/',
                self.admin_site.admin_view(self.page_content_view),
                name='theater_cms_seasonalsponsor_page_content'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Add a button to edit page content
        extra_context['page_content_url'] = reverse('admin:theater_cms_seasonalsponsor_page_content')
        
        # Add custom styling and the page content button
        extra_context['extra_content'] = """
        <div style="margin-bottom: 20px; padding: 15px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px;">
            <h3 style="margin-top: 0; color: #417690;">Sponsors Page Settings</h3>
            <p style="margin-bottom: 15px; color: #666;">Manage the title and introduction text that appears on both English and Chinese sponsors pages.</p>
            <a href="{}" class="button" style="background-color: #417690; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; font-weight: bold;">
                Edit Page Title & Intro Text
            </a>
        </div>
        """.format(extra_context['page_content_url'])
        
        return super().changelist_view(request, extra_context)
    
    def page_content_view(self, request):
        """Custom view for editing sponsors page content"""
        from django import forms
        
        # Get or create the content instance
        content_instance = SponsorsPageContent.get_content()
        
        class SponsorPageContentForm(forms.ModelForm):
            class Meta:
                model = SponsorsPageContent
                fields = ['sponsors_title_en', 'sponsors_intro_en', 'sponsors_title_zh', 'sponsors_intro_zh']
                widgets = {
                    'sponsors_title_en': forms.TextInput(attrs={'style': 'width: 100%; font-size: 16px; padding: 8px;'}),
                    'sponsors_title_zh': forms.TextInput(attrs={'style': 'width: 100%; font-size: 16px; padding: 8px;'}),
                    'sponsors_intro_en': forms.Textarea(attrs={'style': 'width: 100%; min-height: 120px; resize: vertical;', 'rows': 5}),
                    'sponsors_intro_zh': forms.Textarea(attrs={'style': 'width: 100%; min-height: 120px; resize: vertical;', 'rows': 5}),
                }
        
        if request.method == 'POST':
            form = SponsorPageContentForm(request.POST, instance=content_instance)
            if form.is_valid():
                form.save()
                self.message_user(request, "Sponsors page content updated successfully.")
                return redirect('admin:theater_cms_seasonalsponsor_changelist')
        else:
            form = SponsorPageContentForm(instance=content_instance)
        
        context = {
            'form': form,
            'title': 'Edit Sponsors Page Content',
            'subtitle': 'Manage the title and introduction text for both English and Chinese sponsors pages',
            'opts': self.model._meta,
            'has_change_permission': True,
            'extra_style': """
            <style>
                .form-row {
                    margin-bottom: 20px;
                }
                
                .form-row label {
                    display: block;
                    font-weight: bold;
                    margin-bottom: 5px;
                    color: #333;
                }
                
                .fieldset {
                    margin-bottom: 25px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 0;
                }
                
                .fieldset h2 {
                    background-color: #417690;
                    color: white;
                    padding: 10px 15px;
                    margin: 0 0 15px 0;
                    font-size: 14px;
                    border-radius: 4px 4px 0 0;
                }
                
                .fieldset-content {
                    padding: 15px;
                }
                
                .help-text {
                    font-size: 12px;
                    color: #666;
                    margin-top: 5px;
                    font-style: italic;
                }
                
                .submit-row {
                    padding: 15px 0;
                    text-align: right;
                    border-top: 1px solid #ddd;
                    margin-top: 20px;
                }
                
                .cancel-link {
                    margin-right: 10px;
                    color: #666;
                    text-decoration: none;
                }
                
                .cancel-link:hover {
                    text-decoration: underline;
                }
            </style>
            """
        }
        
        return render(request, 'admin/theater_cms/sponsor_page_content.html', context)

# Don't register SponsorsPageContent separately since it's integrated into SeasonalSponsorAdmin

# Register other models
@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    """Admin interface for user feedback that prevents editing of submissions."""
    list_display = ('name', 'rating', 'created_at', 'display_comments')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'comments')
    readonly_fields = ('name', 'rating', 'comments', 'created_at')
    
    def display_comments(self, obj):
        """Truncate long comments for the list view"""
        if len(obj.comments) > 50:
            return f"{obj.comments[:50]}..."
        return obj.comments
    display_comments.short_description = 'Comments'
    
    def has_add_permission(self, request):
        """Prevent admins from manually adding feedback"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing of feedback"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion of inappropriate feedback if needed"""
        return True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        
        # Add a notice explaining why editing is disabled
        extra_context['additional_info'] = """
        <div style="margin: 20px 0; padding: 10px 15px; background-color: #fef9e7; border-left: 4px solid #f1c40f;">
            <h3 style="margin-top: 0; color: #7d6608;">Feedback Integrity Notice</h3>
            <p>User feedback cannot be edited to maintain the integrity and authenticity of customer reviews. 
            This helps ensure transparency and trust in our feedback system.</p>
            <p>Inappropriate content can still be removed using the delete option if necessary.</p>
        </div>
        """
        
        return super().changeform_view(request, object_id, form_url, extra_context)

admin.site.register(EmailSubscription)
