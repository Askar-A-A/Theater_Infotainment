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
    
    # path('home/', views.home_view, name='home'),
    path('sponsors/', views.sponsors_page, name='sponsors_page'),
    path('events/', views.event_list, name='event_list'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('current-event/', views.current_event, name='current_event'),
    path('thank-you/', views.thank_you_page, name='thank_you'),
    
    # Chinese routes
    path('sponsors_zh/', views.sponsors_view_zh, name='sponsors_zh'),
    path('events_zh/', views.events_view_zh, name='events_zh'),
    path('event_zh/<slug:slug>/', views.event_detail_zh, name='event_detail_zh'),
    path('current-event_zh/', views.current_event_zh, name='current_event_zh'),
    path('thank-you_zh/', views.thank_you_zh, name='thank_you_zh'),
] 
