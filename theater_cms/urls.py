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
    path('home/', views.home_view, name='home'),
    path('greetings/', views.greeting_view, name='greetings'),
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
    
    # Arabic routes
    path('home_ar/', views.home_view_ar, name='home_ar'),
    path('greetings_ar/', views.greeting_view_ar, name='greetings_ar'),
    path('intro_ar/', views.intro_view_ar, name='intro_ar'),
    path('feedback_ar/', views.feedback_view_ar, name='feedback_view_ar'),
    path('email-subscribe_ar/', views.email_subscribe_ar, name='email_subscribe_ar'),
    path('about_ar/', views.about_view_ar, name='about_view_ar'),
    path('qa_ar/', views.qa_view_ar, name='qa_view_ar'),
    path('sponsors_ar/', views.sponsors_view_ar, name='sponsors_ar'),
    path('events_ar/', views.events_view_ar, name='events_ar'),
    path('event_ar/<slug:slug>/', views.event_detail_ar, name='event_detail_ar'),
    path('current-event_ar/', views.current_event_ar, name='current_event_ar'),
    path('thank-you_ar/', views.thank_you_ar, name='thank_you_ar'),
    path('email-thank-you_ar/', views.email_thank_you_ar, name='email_thank_you_ar'),
] 
