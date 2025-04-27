from django.contrib import admin
from django import forms
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import Event, Performance, UserFeedback, EmailSubscription
from django.utils.translation import gettext_lazy as _
from django.db import models

class PerformanceInline(admin.TabularInline):
    model = Performance
    extra = 1  # Show only one empty form by default
    fields = ('performance_date', 'performance_time', 'end_time', 'is_special', 'notes')
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
    performance_date.short_description = _("Date")
    
    def performance_time(self, obj):
        if obj and obj.start_time:
            return obj.start_time.time()
        return None
    performance_time.short_description = _("Time")
    
    # Add save_model to combine date and time
    def save_model(self, request, obj, form, change):
        # This won't be called for inline forms, but we'll add a custom formset
        pass
    
    # We need to provide a custom formset to handle the date/time split
    def get_formset(self, request, obj=None, **kwargs):
        from django import forms
        from datetime import datetime, timedelta
        
        # Create a custom form for the inline
        class PerformanceForm(forms.ModelForm):
            # Add separate date and time fields
            performance_date = forms.DateField(
                label=_("Date"),
                widget=forms.DateInput(attrs={'type': 'date'})
            )
            performance_time = forms.TimeField(
                label=_("Time"),
                widget=forms.TimeInput(attrs={'type': 'time'}),
                initial='19:30'
            )
            
            class Meta:
                model = Performance
                fields = ['performance_date', 'performance_time', 'is_special', 'notes']
                
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Pre-populate date and time fields if we have an existing instance
                if self.instance and self.instance.pk and self.instance.start_time:
                    self.fields['performance_date'].initial = self.instance.start_time.date()
                    self.fields['performance_time'].initial = self.instance.start_time.time()
            
            def save(self, commit=True):
                # Don't call save yet
                instance = super().save(commit=False)
                
                # Combine date and time into datetime
                date = self.cleaned_data['performance_date']
                time = self.cleaned_data['performance_time']
                instance.start_time = datetime.combine(date, time)
                
                # Set end time based on duration (default 3 hours)
                if not instance.end_time:
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
        
        # Return the formset with our customizations
        defaults = {
            "formset": CustomInlineFormSet,
            "form": PerformanceForm,
        }
        defaults.update(kwargs)
        return super().get_formset(request, obj, **defaults)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'composer', 'date_range_display', 'performance_count', 'is_active', 'schedule_button')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active',)
    search_fields = ('title', 'composer')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'composer', 'image', 'is_active', 'sort_order')
        }),
        (_('Duration Information'), {
            'fields': ('standard_duration', 'duration'),
            'description': _('Standard duration is used to automatically calculate end times when scheduling performances.')
        }),
        (_('Content Details'), {
            'fields': ('about_content', 'language', 'conductor', 'director', 'cast_content', 'additional_details'),
            'classes': ('collapse',),
        }),
    )
    inlines = [PerformanceInline]
    
    # Add a field for the help text above the inline
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['performance_help_text'] = _(
            "Use 'Schedule Performances' for adding multiple performances more easily. "
            "The section below is for manual adjustments to individual performances."
        )
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
            
            repeat_type = forms.ChoiceField(
                choices=REPEAT_CHOICES, 
                widget=forms.RadioSelect,
                initial='single',
                label=_("Scheduling Type")
            )
            
            # Single Performance Fields
            single_date = forms.DateField(
                widget=forms.DateInput(attrs={'type': 'date'}),
                label=_("Performance Date"),
                help_text=_("Date for this performance"),
                required=False
            )
            single_time = forms.TimeField(
                widget=forms.TimeInput(attrs={'type': 'time'}),
                initial='19:30',
                label=_("Performance Time"),
                help_text=_("Start time (e.g., 19:30)"),
                required=False
            )
            
            # Weekly Performance Fields
            weekly_first_date = forms.DateField(
                widget=forms.DateInput(attrs={'type': 'date'}),
                label=_("First Performance"),
                help_text=_("Date of the first performance"),
                required=False
            )
            weekly_time = forms.TimeField(
                widget=forms.TimeInput(attrs={'type': 'time'}),
                initial='19:30',
                label=_("Performance Time"),
                help_text=_("Start time for all performances"),
                required=False
            )
            weekly_end_date = forms.DateField(
                widget=forms.DateInput(attrs={'type': 'date'}),
                label=_("Last Performance"),
                help_text=_("Date of the last weekly performance"),
                required=False
            )
            
            # Custom Dates Field
            custom_dates = forms.CharField(
                widget=forms.Textarea(attrs={
                    'rows': 5,
                    'placeholder': '2025-04-26 19:30\n2025-04-29 20:00\n2025-04-31 14:00'
                }),
                label=_("Performance Dates and Times"),
                help_text=_("Enter each performance on a new line as: YYYY-MM-DD HH:MM"),
                required=False
            )
            
            # Common Fields
            duration = forms.DurationField(
                required=False,
                label=_("Performance Duration"),
                help_text=_("Duration in hours:minutes (e.g., 2:30). Leave blank to use event's standard duration.")
            )
            
            notes = forms.CharField(
                required=False,
                widget=forms.TextInput(),
                label=_("Performance Notes"),
                help_text=_("Special notes to apply to all created performances (e.g., 'With English subtitles')")
            )
            
            def clean(self):
                cleaned_data = super().clean()
                repeat_type = cleaned_data.get('repeat_type')
                
                if repeat_type == 'single':
                    if not cleaned_data.get('single_date'):
                        self.add_error('single_date', _("Required for single performance"))
                    if not cleaned_data.get('single_time'):
                        self.add_error('single_time', _("Required for single performance"))
                    
                elif repeat_type == 'weekly':
                    if not cleaned_data.get('weekly_first_date'):
                        self.add_error('weekly_first_date', _("Required for weekly performances"))
                    if not cleaned_data.get('weekly_time'):
                        self.add_error('weekly_time', _("Required for weekly performances"))
                    if not cleaned_data.get('weekly_end_date'):
                        self.add_error('weekly_end_date', _("Required for weekly performances"))
                    
                elif repeat_type == 'custom':
                    if not cleaned_data.get('custom_dates'):
                        self.add_error('custom_dates', _("Please enter at least one date"))
                    
                return cleaned_data
        
        if request.method == 'POST':
            form = BulkScheduleForm(request.POST)
            if form.is_valid():
                from datetime import datetime, timedelta
                
                repeat_type = form.cleaned_data['repeat_type']
                duration = form.cleaned_data['duration'] or timedelta(hours=3)
                notes = form.cleaned_data['notes']
                
                performances_to_create = []
                
                if repeat_type == 'single':
                    date = form.cleaned_data['single_date']
                    time = form.cleaned_data['single_time']
                    start_time = datetime.combine(date, time)
                    
                    performances_to_create.append({
                        'start_time': start_time,
                        'end_time': start_time + duration,
                        'notes': notes
                    })
                    
                elif repeat_type == 'weekly':
                    first_date = form.cleaned_data['weekly_first_date']
                    time = form.cleaned_data['weekly_time']
                    end_date = form.cleaned_data['weekly_end_date']
                    
                    current_date = first_date
                    while current_date <= end_date:
                        start_time = datetime.combine(current_date, time)
                        performances_to_create.append({
                            'start_time': start_time,
                            'end_time': start_time + duration,
                            'notes': notes
                        })
                        current_date += timedelta(days=7)  # Next week
                        
                elif repeat_type == 'custom':
                    custom_dates_text = form.cleaned_data['custom_dates']
                    for line in custom_dates_text.split('\n'):
                        line = line.strip()
                        if not line:
                            continue
                            
                        try:
                            # Expect format: "YYYY-MM-DD HH:MM"
                            date_str = line
                            custom_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                            
                            performances_to_create.append({
                                'start_time': custom_datetime,
                                'end_time': custom_datetime + duration,
                                'notes': notes
                            })
                        except ValueError:
                            # Skip invalid lines
                            continue
                
                # Create all performances
                for perf_data in performances_to_create:
                    Performance.objects.create(
                        event=event,
                        start_time=perf_data['start_time'],
                        end_time=perf_data['end_time'],
                        notes=perf_data['notes']
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
    list_display = ('event', 'start_time', 'end_time', 'is_special', 'notes')
    list_filter = ('event', 'start_time', 'is_special')
    search_fields = ('event__title', 'notes')
    date_hierarchy = 'start_time'

# Register other models
admin.site.register(UserFeedback)
admin.site.register(EmailSubscription)
