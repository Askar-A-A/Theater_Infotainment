from django.urls import path
from . import views

app_name = 'user_interactions'

urlpatterns = [
    # Language switching
    path('switch-language/', views.switch_language, name='switch_language'),
    
    # Form processing (language-neutral)
    path('process_feedback/', views.process_feedback, name='process_feedback'),
    path('process_subscription/', views.process_subscription, name='process_subscription'),
    path('clear_subscription_messages/', views.clear_subscription_messages, name='clear_subscription_messages'),
    
    # English routes (default)
    path('home/', views.home_view, name='home'),
    path('sponsors/', views.sponsors_page, name='sponsors_page'),
    path('events/', views.event_list, name='event_list'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('current-event/', views.current_event, name='current_event'),
    path('current-event_lt/', views.current_event_lt, name='current_event_lt'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('about/', views.about_view, name='about'),
    path('email/', views.email_subscribe, name='email_subscribe'),
    path('qa/', views.qa_view, name='qa'),
    path('thank-you/', views.thank_you_page, name='thank_you'),
    
    # Lithuanian routes
    path('home_lt/', views.home_view_lt, name='home_lt'),
    path('greeting_lt/', views.greeting_view_lt, name='greeting_lt'),
    path('sponsors_lt/', views.sponsors_view_lt, name='sponsors_lt'),
    path('events_lt/', views.events_view_lt, name='events_lt'),
    path('event_lt/<slug:slug>/', views.event_detail_lt, name='event_detail_lt'),
    path('current-event_lt/', views.current_event_lt, name='current_event_lt'),
    path('feedback_lt/', views.feedback_view_lt, name='feedback_lt'),
    path('about_lt/', views.about_view_lt, name='about_lt'),
    path('email-subscribe_lt/', views.email_subscribe_lt, name='email_subscribe_lt'),
    path('qa_lt/', views.qa_view_lt, name='qa_lt'),
    path('thank-you_lt/', views.thank_you_lt, name='thank_you_lt'),
] 
