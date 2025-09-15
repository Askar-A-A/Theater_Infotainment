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
    
    # Lithuanian routes
    path('intro_lt/', views.intro_view_lt, name='intro_lt'),
    path('feedback_lt/', views.feedback_view_lt, name='feedback_view_lt'),
    path('email-subscribe_lt/', views.email_subscribe_lt, name='email_subscribe_lt'),
    path('about_lt/', views.about_view_lt, name='about_view_lt'),
    path('qa_lt/', views.qa_view_lt, name='qa_view_lt'),
    path('sponsors_lt/', views.sponsors_view_lt, name='sponsors_lt'),
    path('events_lt/', views.events_view_lt, name='events_lt'),
    path('event_lt/<slug:slug>/', views.event_detail_lt, name='event_detail_lt'),
    path('current-event_lt/', views.current_event_lt, name='current_event_lt'),
    path('thank-you_lt/', views.thank_you_lt, name='thank_you_lt'),
    path('email-thank-you_lt/', views.email_thank_you_lt, name='email_thank_you_lt'),
] 
