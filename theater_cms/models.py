from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

# Models for custom plugins

class TheaterLogo(CMSPlugin):
    image = FilerImageField(
        verbose_name="Theater Logo",
        on_delete=models.CASCADE,
        related_name="theater_logo"
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alternative text for the logo"
    )

    def __str__(self):
        return self.alt_text or "Theater Logo"

class SponsorLogo(CMSPlugin):
    """Plugin for adding sponsor logos to the sponsors page"""
    image = FilerImageField(
        verbose_name="Sponsor Logo",
        on_delete=models.CASCADE,
        related_name="sponsor_logos"
    )
    name = models.CharField(
        max_length=100,
        help_text="Sponsor name for alt text and accessibility"
    )
    
    def __str__(self):
        return self.name

class EventCard(CMSPlugin):
    """Plugin for displaying event information in the events grid"""
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
    image = FilerImageField(
        verbose_name="Event Image",
        on_delete=models.CASCADE,
        related_name="event_images"
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

class QAItemPlugin(CMSPlugin):
    question = models.TextField(
        verbose_name="Question"
    )
    answer = models.TextField(
        verbose_name="Answer",
        help_text="You may use HTML for formatting"
    )
    
    def __str__(self):
        return self.question
    

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    composer = models.CharField(max_length=100, blank=True)
    about_content = models.TextField(blank=True)
    language = models.CharField(max_length=100, blank=True)
    conductor = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=100, blank=True)
    cast_content = models.TextField(blank=True)
    duration = models.CharField(max_length=50, blank=True)
    
    # Chinese translation fields (new)
    title_zh = models.CharField(max_length=200, blank=True, verbose_name="Title (Chinese)", 
                               help_text="Chinese translation of the event title")
    composer_zh = models.CharField(max_length=100, blank=True, verbose_name="Composer (Chinese)",
                                  help_text="Chinese translation of composer name")
    about_content_zh = models.TextField(blank=True, verbose_name="About Content (Chinese)",
                                       help_text="Chinese translation of the about content")
    language_zh = models.CharField(max_length=100, blank=True, verbose_name="Language (Chinese)",
                                  help_text="e.g., '意大利语配中文字幕'")
    conductor_zh = models.CharField(max_length=100, blank=True, verbose_name="Conductor (Chinese)",
                                   help_text="Chinese translation of conductor name")
    director_zh = models.CharField(max_length=100, blank=True, verbose_name="Director (Chinese)",
                                  help_text="Chinese translation of director name")
    cast_content_zh = models.TextField(blank=True, verbose_name="Cast Content (Chinese)",
                                      help_text="Chinese translation of cast information")
    duration_zh = models.CharField(max_length=50, blank=True, verbose_name="Duration (Chinese)",
                                  help_text="e.g., '约3小时（含休息时间）'")
    
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    standard_duration = models.DurationField(blank=True, null=True)
    additional_details = models.TextField(blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    date_range_display = models.CharField(max_length=200, blank=True)
    
    # Helper methods for language-aware content
    def get_title(self, language='en'):
        if language == 'zh' and self.title_zh:
            return self.title_zh
        return self.title
    
    def get_composer(self, language='en'):
        if language == 'zh' and self.composer_zh:
            return self.composer_zh
        return self.composer
    
    def get_about_content(self, language='en'):
        if language == 'zh' and self.about_content_zh:
            return self.about_content_zh
        return self.about_content
    
    def get_language(self, language='en'):
        if language == 'zh' and self.language_zh:
            return self.language_zh
        return self.language
    
    def get_conductor(self, language='en'):
        if language == 'zh' and self.conductor_zh:
            return self.conductor_zh
        return self.conductor
    
    def get_director(self, language='en'):
        if language == 'zh' and self.director_zh:
            return self.director_zh
        return self.director
    
    def get_cast_content(self, language='en'):
        if language == 'zh' and self.cast_content_zh:
            return self.cast_content_zh
        return self.cast_content
    
    def get_duration(self, language='en'):
        if language == 'zh' and self.duration_zh:
            return self.duration_zh
        return self.duration
    
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
        verbose_name = "Event"
        verbose_name_plural = "Events"

class Performance(models.Model):
    """Individual performance/showing of an event"""
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name='performances'
    )
    start_time = models.DateTimeField("Start Time")
    end_time = models.DateTimeField("End Time", blank=True, null=True)

    class Meta:
        ordering = ['start_time']
        verbose_name = "Performance"
        verbose_name_plural = "Performances"
    
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

    def __str__(self):
        return self.name

class SponsorPageContent(models.Model):
    """Singleton model for storing sponsors page content"""
    # English content
    title = models.CharField(
        max_length=200, 
        default="Our Esteemed Sponsors",
        verbose_name="Page Title (English)",
        help_text="Main title displayed on the sponsors page"
    )
    intro_text = models.TextField(
        default="Our theater is proud to acknowledge the generous support of our sponsors. Their commitment to the arts enables us to continue our tradition of excellence and share the magic of opera with audiences from around the world.",
        verbose_name="Introduction Text (English)",
        help_text="Introduction text displayed below the title"
    )
    
    # Russian content
    title_ru = models.CharField(
        max_length=200,
        default="Наши уважаемые спонсоры", 
        verbose_name="Page Title (Russian)",
        help_text="Main title displayed on the Russian sponsors page"
    )
    intro_text_ru = models.TextField(
        default="Наш театр с гордостью благодарит спонсоров за их щедрую поддержку. Их приверженность искусству позволяет нам продолжать традиции совершенства и делиться магией оперы с аудиторией со всего мира.",
        verbose_name="Introduction Text (Russian)", 
        help_text="Introduction text displayed below the title on Russian page"
    )
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the singleton instance
        pass

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return "Sponsors Page Content"
    
    class Meta:
        verbose_name = "Sponsor Page Content"
        verbose_name_plural = "Sponsor Page Content"