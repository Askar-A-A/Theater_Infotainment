from django.urls import path
from . import views

app_name = 'user_interactions'

urlpatterns = [
    # This is just for processing the form, not rendering the template
    path('process_feedback/', views.process_feedback, name='process_feedback'),
    path('thank-you/', views.thank_you_page, name='thank_you'),
    path('process_subscription/', views.process_subscription, name='process_subscription'),
    path('clear_subscription_messages/', views.clear_subscription_messages, name='clear_subscription_messages'),
    
    # New URLs for events
    path('events/', views.event_list, name='event_list'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('current-event/', views.current_event, name='current_event'),
    path('sponsors/', views.sponsors_page, name='sponsors_page'),
    
    # New static page URLs (to replace CMS pages)
    path('', views.greeting_page, name='greeting'),
    path('home/', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('qa/', views.qa_page, name='qa'),
    path('email_subscribe/', views.email_subscribe_page, name='email_subscribe'),
    path('feedback/', views.feedback_page, name='feedback'),
] 
