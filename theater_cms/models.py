from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Converted plugin models to regular Django models

class TheaterLogo(models.Model):
    image = models.ImageField(
        verbose_name="Theater Logo",
        upload_to="theater_logos/",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alternative text for the logo"
    )

    def __str__(self):
        return self.alt_text or "Theater Logo"

class SponsorLogo(models.Model):
    """Model for adding sponsor logos to the sponsors page"""
    image = models.ImageField(
        verbose_name="Sponsor Logo",
        upload_to="sponsor_logos/"
    )
    name = models.CharField(
        max_length=100,
        help_text="Sponsor name for alt text and accessibility"
    )
    website = models.URLField(
        blank=True,
        help_text="Optional link to sponsor website"
    )
    
    def __str__(self):
        return self.name

class EventCard(models.Model):
    """Model for displaying event information in the events grid"""
    title = models.CharField(
        max_length=200,
        help_text="Event title (e.g., 'Tosca')"
    )
    composer = models.CharField(
        max_length=200,
        help_text="Composer name (e.g., 'Giacomo Puccini')"
    )
    date_range = models.CharField(
        max_length=200,
        help_text="Performance dates (e.g., 'January 15 - March 30, 2024')"
    )
    image = models.ImageField(
        verbose_name="Event Image",
        upload_to="event_cards/"
    )
    detail_url = models.URLField(
        blank=True,
        help_text="Optional link to event detail page"
    )
    
    def __str__(self):
        return self.title
    

# Models for user interaction/data

class UserFeedback(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Star'),
        (3, '3 Star'),
        (4, '4 Star'),
        (5, '5 Star')
    )
    name = models.CharField(max_length=50, blank=True, verbose_name="Name (Optional)")
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True, verbose_name="User Rating")
    comments = models.TextField(max_length=500, verbose_name="User Feedback")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback from {self.name or 'Anonymous'} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback Entries"

class EmailSubscription(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    name = models.CharField(max_length=100, blank=True, verbose_name="Name (Optional)")
    receive_updates = models.BooleanField(default=True, verbose_name="Receive Updates")
    subscribed_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.email} ({self.name})" if self.name else self.email
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Email Subscription"
        verbose_name_plural = "Email Subscriptions"

# Convert QA plugin to regular model
class QAItem(models.Model):
    question = models.CharField(
        max_length=255,
        verbose_name=_("Question")
    )
    answer = models.TextField(
        verbose_name=_("Answer"),
        help_text=_("You may use HTML for formatting")
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['order']
        verbose_name = _("Q&A Item")
        verbose_name_plural = _("Q&A Items")

class Event(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    composer = models.CharField(_("Composer"), max_length=200)
    image = models.ImageField(_("Event Image"), upload_to='events/', blank=True, null=True)  
    
    # These will be calculated automatically based on performances
    start_datetime = models.DateTimeField(_("First Performance"), blank=True, null=True, editable=False)
    end_datetime = models.DateTimeField(_("Last Performance"), blank=True, null=True, editable=False)
    date_range_display = models.CharField(_("Date Range"), max_length=200, blank=True, editable=False)

    # Standard show duration (for scheduling help)
    standard_duration = models.DurationField(
        _("Standard Duration"),
        blank=True, null=True,
        help_text=_("Standard duration of a performance (e.g., '02:30:00' for 2.5 hours)")
    )

    about_content = models.TextField(_("About"), blank=True)
    duration = models.CharField(_("Duration Display Text"), max_length=200, blank=True)
    language = models.CharField(_("Language"), max_length=200, blank=True)
    conductor = models.CharField(_("Conductor"), max_length=200, blank=True)
    director = models.CharField(_("Director"), max_length=200, blank=True)
    cast_content = models.TextField(_("Cast"), blank=True)
    additional_details = models.TextField(_("Additional Details"), blank=True)

    is_active = models.BooleanField(_("Active"), default=True)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('user_interactions:event_detail', kwargs={'slug': self.slug})
    
    def update_date_range(self):
        """Update the start/end times and date range display based on performances"""
        performances = self.performances.all().order_by('start_time')
        
        if not performances:
            return
            
        first_performance = performances.first()
        last_performance = performances.last()
        
        # Update first and last performance dates
        self.start_datetime = first_performance.start_time
        self.end_datetime = last_performance.end_time
        
        # Create a human-readable date range
        first_date = first_performance.start_time.strftime('%B %d')
        last_date = last_performance.start_time.strftime('%B %d, %Y')
        
        # If same year, don't repeat year in first date
        if first_performance.start_time.year == last_performance.start_time.year:
            self.date_range_display = f"{first_date} - {last_date}"
        else:
            first_date_with_year = first_performance.start_time.strftime('%B %d, %Y')
            self.date_range_display = f"{first_date_with_year} - {last_date}"
            
        # Save without calling this method again
        Event.objects.filter(pk=self.pk).update(
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            date_range_display=self.date_range_display
        )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['sort_order', 'start_datetime']
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

class Performance(models.Model):
    """Individual performance/showing of an event"""
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name='performances'
    )
    start_time = models.DateTimeField(_("Start Time"))
    end_time = models.DateTimeField(_("End Time"), blank=True, null=True)

    class Meta:
        ordering = ['start_time']
        verbose_name = _("Performance")
        verbose_name_plural = _("Performances")
    
    def __str__(self):
        return f"{self.event.title} - {self.start_time.strftime('%d %b %Y, %H:%M')}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate end time if not provided (default 3 hours after start)
        if not self.end_time and self.start_time:
            from datetime import timedelta
            self.end_time = self.start_time + timedelta(hours=3)
        super().save(*args, **kwargs)
        
        # Update the parent event's date range
        self.event.update_date_range()

class SeasonalSponsor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='seasonal_sponsors/', blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class EventSponsorImage(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='sponsor_images',
        verbose_name="Event",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_sponsors/', blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class SiteSettings(models.Model):
    """Single-instance model to store site-wide settings."""
    display_height = models.IntegerField(
        choices=[
            (800, '1280 × 800px (Full Size)'),
            (400, '1280 × 400px (Compact)'),
            (600, '1024 × 600px (Medium)')
        ],
        default=800,
        help_text="Select the display height for all theater screens."
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        width = "1280"
        if self.display_height == 600:
            width = "1024"
        return f"Site Settings - {width}×{self.display_height}px (Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M')})"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_solo(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj