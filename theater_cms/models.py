from django.db import models
from django.utils import timezone
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from django.utils.translation import gettext_lazy as _

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
    website = models.URLField(
        blank=True,
        help_text="Optional link to sponsor website"
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
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True, verbose_name="Your rating")
    comments = models.TextField(max_length=500, verbose_name="Your Feedback")
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
    question = models.CharField(
        max_length=255,
        verbose_name=_("Question")
    )
    answer = models.TextField(
        verbose_name=_("Answer"),
        help_text=_("You may use HTML for formatting")
    )
    
    def __str__(self):
        return self.question