from django.urls import path
from . import views

app_name = 'user_interactions'

urlpatterns = [
    # Form processing (language-neutral)
    path('process_feedback/', views.process_feedback, name='process_feedback'),
    path('process_subscription/', views.process_subscription, name='process_subscription'),
    path('clear_subscription_messages/', views.clear_subscription_messages, name='clear_subscription_messages'),
    path('clear_feedback_messages/', views.clear_feedback_messages, name='clear_feedback_messages'),
    
    # English routes (default)
    # path('home/', views.home_view, name='home'),
    path('intro/', views.intro_view, name='intro'),
    path('feedback/', views.feedback_view, name='feedback_view'),
    path('email-subscribe/', views.email_subscribe, name='email_subscribe'),
    path('about/', views.about_view, name='about_view'),
    path('qa/', views.qa_view, name='qa_view'),
    path('sponsors/', views.sponsors_page, name='sponsors_page'),
    path('events/', views.event_list, name='event_list'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('current-event/', views.current_event, name='current_event'),
    path('thank-you/', views.thank_you_page, name='thank_you_page'),
    path('email-thank-you/', views.email_thank_you_page, name='email_thank_you_page'),
    
    # Russian routes
    path('intro_ru/', views.intro_view_ru, name='intro_ru'),
    path('feedback_ru/', views.feedback_view_ru, name='feedback_view_ru'),
    path('email-subscribe_ru/', views.email_subscribe_ru, name='email_subscribe_ru'),
    path('about_ru/', views.about_view_ru, name='about_view_ru'),
    path('qa_ru/', views.qa_view_ru, name='qa_view_ru'),
    path('sponsors_ru/', views.sponsors_view_ru, name='sponsors_ru'),
    path('events_ru/', views.events_view_ru, name='events_ru'),
    path('event_ru/<slug:slug>/', views.event_detail_ru, name='event_detail_ru'),
    path('current-event_ru/', views.current_event_ru, name='current_event_ru'),
    path('thank-you_ru/', views.thank_you_ru, name='thank_you_ru'),
    path('email-thank-you_ru/', views.email_thank_you_ru, name='email_thank_you_ru'),
] 
