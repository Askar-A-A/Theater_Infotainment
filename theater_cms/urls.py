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
    path('current-event_ru/', views.current_event_ru, name='current_event_ru'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('about/', views.about_view, name='about'),
    path('email/', views.email_subscribe, name='email_subscribe'),
    path('qa/', views.qa_view, name='qa'),
    path('thank-you/', views.thank_you_page, name='thank_you'),
    
    # Russian routes
    path('home_ru/', views.home_view_ru, name='home_ru'),
    path('greeting_ru/', views.greeting_view_ru, name='greeting_ru'),
    path('sponsors_ru/', views.sponsors_view_ru, name='sponsors_ru'),
    path('events_ru/', views.events_view_ru, name='events_ru'),
    path('event_ru/<slug:slug>/', views.event_detail_ru, name='event_detail_ru'),
    path('current-event_ru/', views.current_event_ru, name='current_event_ru'),
    path('feedback_ru/', views.feedback_view_ru, name='feedback_ru'),
    path('about_ru/', views.about_view_ru, name='about_ru'),
    path('email-subscribe_ru/', views.email_subscribe_ru, name='email_subscribe_ru'),
    path('qa_ru/', views.qa_view_ru, name='qa_ru'),
    path('thank-you_ru/', views.thank_you_ru, name='thank_you_ru'),
] 
