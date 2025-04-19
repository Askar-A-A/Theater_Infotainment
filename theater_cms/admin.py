from django.contrib import admin
from .models import UserFeedback, EmailSubscription

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at', 'short_comments')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'comments')
    
    def short_comments(self, obj):
        if len(obj.comments) > 50:
            return obj.comments[:50] + "..."
        return obj.comments
    
    short_comments.short_description = "Comments"

@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'receive_updates', 'subscribed_at')
    list_filter = ('receive_updates', 'subscribed_at')
    search_fields = ('email', 'name')
    date_hierarchy = 'subscribed_at'
