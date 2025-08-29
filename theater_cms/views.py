from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserFeedback, EmailSubscription, Event, Performance, SeasonalSponsor, EventSponsorImage, SponsorsPageContent
from cms.utils import get_current_site
from django.views.decorators.http import require_POST
from django.utils import timezone

def process_feedback(request):
    # Only process POST requests
    if request.method != 'POST':
        # If accessed directly via GET, redirect back to the feedback page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    # Extract form data
    name = request.POST.get('name', '')
    rating = request.POST.get('rating', None)
    comments = request.POST.get('comments', '')
    
    # Validate data
    errors = {}
    
    if not comments.strip():
        errors['comments'] = "Please provide your feedback."
    
    if rating == '0' or not rating:
        errors['rating'] = "Please select a rating."
    elif not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        errors['rating'] = "Please select a valid rating."
    
    # If there are errors, store them in session and redirect back
    if errors:
        request.session['feedback_errors'] = errors
        request.session['feedback_data'] = {
            'name': name,
            'rating': rating,
            'comments': comments
        }
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # If valid, save the feedback
    rating_int = int(rating)
    
    UserFeedback.objects.create(
        name=name,
        rating=rating_int,
        comments=comments
    )
    
    # Clear any stored errors/data
    if 'feedback_errors' in request.session:
        del request.session['feedback_errors']
    if 'feedback_data' in request.session:
        del request.session['feedback_data']
    
    # Redirect to appropriate thank you page based on language
    user_language = request.session.get('user_language', 'en')
    if user_language == 'zh':
        return redirect('/thank-you_zh/')
    else:
        return redirect('/thank-you/')

def thank_you_page(request):
    """
    English thank you page - uses the regular template
    """
    return render(request, 'feedback_thank_you.html')

def process_subscription(request):
    """Process email subscription form submissions."""
    # Only process POST requests
    if request.method != 'POST':
        # If accessed directly via GET, redirect back
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    # Extract form data
    email = request.POST.get('email', '')
    name = request.POST.get('name', '')
    preferences = request.POST.get('preferences', '') == 'on'  # Convert checkbox to boolean
    
    # Validate data
    errors = {}
    
    if not email or '@' not in email:
        errors['email'] = "Please provide a valid email address."
    
    # If there are errors, store them in session and redirect back
    if errors:
        request.session['subscription_errors'] = errors
        request.session['subscription_data'] = {
            'email': email,
            'name': name,
            'preferences': preferences
        }
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # Check if email already exists
    if EmailSubscription.objects.filter(email=email).exists():
        # Get user language for appropriate message
        user_language = request.session.get('user_language', 'en')
        if user_language == 'zh':
            request.session['subscription_warning'] = "您已经订阅了我们的新闻通讯。"
        else:
            request.session['subscription_warning'] = "You are already subscribed to our newsletter."
        
        # Store the email for display but clear other data
        request.session['subscription_data'] = {
            'email': email,
            'name': name,
            'preferences': preferences
        }
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # If valid, save the subscription
    EmailSubscription.objects.create(
        email=email,
        name=name,
        receive_updates=preferences
    )
    
    # Clear any stored errors/data/warnings
    session_keys_to_clear = [
        'subscription_errors', 
        'subscription_data', 
        'subscription_warning'
    ]
    for key in session_keys_to_clear:
        if key in request.session:
            del request.session[key]
    
    # Set success message
    request.session['subscription_success'] = True
    
    # Redirect back to the same page to show success message
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def clear_subscription_messages(request):
    """Clear subscription success/message flags from session."""
    try:
        # Clear all subscription-related session data
        session_keys_to_clear = [
            'subscription_success',
            'subscription_message',
            'subscription_warning',
            'subscription_errors',
            'subscription_data'
        ]
        
        cleared_keys = []
        for key in session_keys_to_clear:
            if key in request.session:
                del request.session[key]
                cleared_keys.append(key)
        
        # Ensure session is saved
        request.session.modified = True
        
        return JsonResponse({
            'status': 'success',
            'cleared_keys': cleared_keys,
            'message': 'Subscription messages cleared successfully'
        })
    except Exception as e:
        # Return success even on error to prevent client-side issues
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def determine_current_event():
    """Utility function to find the current or next event"""
    now = timezone.now()
    
    # First check for events with performances happening right now
    current_performances = Performance.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        event__is_active=True
    ).select_related('event').order_by('start_time')
    
    if current_performances.exists():
        return current_performances.first().event
    
    # If no current performances, find the next upcoming performance
    upcoming_performances = Performance.objects.filter(
        start_time__gt=now,
        event__is_active=True
    ).select_related('event').order_by('start_time')
    
    if upcoming_performances.exists():
        return upcoming_performances.first().event
    
    # If no upcoming performances, return the most recent past performance
    past_performances = Performance.objects.filter(
        end_time__lt=now,
        event__is_active=True
    ).select_related('event').order_by('-end_time')
    
    if past_performances.exists():
        return past_performances.first().event
    
    return None

def event_list(request):
    """View for the events listing page"""
    events = Event.objects.filter(is_active=True).order_by('sort_order', 'start_datetime')
    return render(request, 'events.html', {'events': events})

def event_detail(request, slug):
    """View for a specific event's details"""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    
    # Get upcoming performances for this event
    now = timezone.now()
    upcoming_performances = event.performances.filter(start_time__gt=now).order_by('start_time')
    
    # Get all distinct dates that have performances
    performance_dates = event.performances.dates('start_time', 'day')
    
    return render(request, 'event_detail.html', {
        'event': event,
        'upcoming_performances': upcoming_performances,
        'performance_dates': performance_dates,
    })

def current_event(request):
    """Redirect to the current event's detail page"""
    event = determine_current_event()
    if event:
        return redirect(event.get_absolute_url())
    else:
        # If no events found, redirect to events list
        return redirect('user_interactions:event_list')

def home_with_current_event(request):
    """Context processor to add current event to home page"""
    event = determine_current_event()
    return {'current_event': event}

def sponsors_page(request):
    """English version"""
    request.session['user_language'] = 'en'
    seasonal_sponsors = SeasonalSponsor.objects.all()
    event = determine_current_event()
    event_sponsors = []
    if event:
        event_sponsors = event.sponsor_images.all()
    
    # Get sponsors page content
    sponsors_content = SponsorsPageContent.get_content()

    return render(request, 'sponsors.html', {
        'seasonal_sponsors': seasonal_sponsors,
        'event_sponsors': event_sponsors,
        'event': event,
        'sponsors_content': sponsors_content,
    })

def switch_language(request):
    """Simple language switching without complex i18n"""
    if request.method != 'POST':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    language = request.POST.get('language', 'en')
    next_page = request.POST.get('next', '/')
    
    # Store language choice in session
    request.session['user_language'] = language
    
    # Simple redirect logic based on current page and target language
    if language == 'zh':
        # Redirect to Chinese version
        if '/sponsors/' in next_page:
            return redirect('/sponsors_zh/')
        elif '/events/' in next_page:
            return redirect('/events_zh/')
        elif '/feedback/' in next_page:
            return redirect('/feedback_zh/')
        elif '/about/' in next_page:
            return redirect('/about_zh/')
        elif '/email/' in next_page:
            return redirect('/email-subscribe_zh/')
        elif '/qa/' in next_page or '/q&a/' in next_page:
            return redirect('/qa_zh/')
        elif '/home/' in next_page:
            return redirect('/home_zh/')
        else:
            # Default to Chinese greeting page
            return redirect('/greeting_zh/')
    else:
        # Redirect to English version (remove _zh suffix)
        if '_zh/' in next_page:
            clean_path = next_page.replace('_zh/', '/', 1)
            if clean_path == '/qa/':
                clean_path = '/q&a/'
            elif clean_path == '/email-subscribe/':
                clean_path = '/email/'
            return redirect(clean_path)
        else:
            return redirect(next_page)

# Language-specific view functions for Chinese versions
def greeting_view_zh(request):
    """Chinese version of greeting page"""
    request.session['user_language'] = 'zh'
    return render(request, 'greeting_zh.html')

def sponsors_view_zh(request):
    """Chinese version of sponsors page"""
    request.session['user_language'] = 'zh'
    seasonal_sponsors = SeasonalSponsor.objects.all()
    event = determine_current_event()
    event_sponsors = []
    if event:
        event_sponsors = event.sponsor_images.all()
    
    # Get sponsors page content
    sponsors_content = SponsorsPageContent.get_content()

    return render(request, 'sponsors_zh.html', {
        'seasonal_sponsors': seasonal_sponsors,
        'event_sponsors': event_sponsors,
        'event': event,
        'sponsors_content': sponsors_content,
    })

def events_view_zh(request):
    """Chinese version of events page"""
    request.session['user_language'] = 'zh'
    events = Event.objects.filter(is_active=True).order_by('sort_order', 'start_datetime')
    
    # Add Chinese content for each event
    events_with_zh = []
    for event in events:
        event_dict = {
            'event': event,
            'title_zh': event.get_title('zh'),
            'composer_zh': event.get_composer('zh'),
        }
        events_with_zh.append(event_dict)
    
    return render(request, 'events_zh.html', {'events_with_zh': events_with_zh})

def event_detail_zh(request, slug):
    """Chinese version of event detail page"""
    request.session['user_language'] = 'zh'
    event = get_object_or_404(Event, slug=slug, is_active=True)
    
    now = timezone.now()
    upcoming_performances = event.performances.filter(start_time__gt=now).order_by('start_time')
    performance_dates = event.performances.dates('start_time', 'day')
    
    # Pre-process Chinese content
    context = {
        'event': event,
        'upcoming_performances': upcoming_performances,
        'performance_dates': performance_dates,
        'event_title_zh': event.get_title('zh'),
        'event_composer_zh': event.get_composer('zh'),
        'event_about_zh': event.get_about_content('zh'),
        'event_language_zh': event.get_language('zh'),
        'event_conductor_zh': event.get_conductor('zh'),
        'event_director_zh': event.get_director('zh'),
        'event_cast_zh': event.get_cast_content('zh'),
        'event_duration_zh': event.get_duration('zh'),
    }
    
    return render(request, 'event_detail_zh.html', context)

def feedback_view_zh(request):
    """Chinese version of feedback page"""
    request.session['user_language'] = 'zh'
    return render(request, 'feedback_zh.html')

def about_view_zh(request):
    """Chinese version of about page"""
    request.session['user_language'] = 'zh'
    return render(request, 'about_zh.html')

def email_subscribe_zh(request):
    """Chinese version of email subscribe page"""
    request.session['user_language'] = 'zh'
    
    # Clear old messages if user navigates back to subscription page
    # This provides a fallback if JavaScript clearing fails
    if not request.session.get('subscription_success') and not request.session.get('subscription_message'):
        # Only clear if there are no active messages to display
        session_keys_to_clear = ['subscription_errors', 'subscription_data']
        for key in session_keys_to_clear:
            if key in request.session:
                del request.session[key]
    
    return render(request, 'email_subscribe_zh.html')

def qa_view_zh(request):
    """Chinese version of Q&A page"""
    request.session['user_language'] = 'zh'
    return render(request, 'q&a_zh.html')

def thank_you_zh(request):
    """Chinese version of thank you page"""
    request.session['user_language'] = 'zh'
    return render(request, 'feedback_thank_you_zh.html')

def home_view_zh(request):
    """Chinese version of home page"""
    request.session['user_language'] = 'zh'
    event = determine_current_event()
    return render(request, 'home_zh.html', {'current_event': event})

def home_view(request):
    """English version of home page"""
    request.session['user_language'] = 'en'
    event = determine_current_event()
    return render(request, 'home.html', {'current_event': event})

def feedback_view(request):
    """English version of feedback page"""
    request.session['user_language'] = 'en'
    return render(request, 'feedback.html')

def about_view(request):
    """English version of about page"""
    request.session['user_language'] = 'en'
    return render(request, 'about.html')

def email_subscribe(request):
    """English version of email subscribe page"""
    request.session['user_language'] = 'en'
    
    # Clear old messages if user navigates back to subscription page
    # This provides a fallback if JavaScript clearing fails
    if not request.session.get('subscription_success') and not request.session.get('subscription_message'):
        # Only clear if there are no active messages to display
        session_keys_to_clear = ['subscription_errors', 'subscription_data']
        for key in session_keys_to_clear:
            if key in request.session:
                del request.session[key]
    
    return render(request, 'email_subscribe.html')

def qa_view(request):
    """English version of Q&A page"""
    request.session['user_language'] = 'en'
    return render(request, 'q&a.html')

def current_event_zh(request):
    """Redirect to the current event's detail page (Chinese)"""
    event = determine_current_event()
    if event:
        return redirect(reverse('user_interactions:event_detail_zh', kwargs={'slug': event.slug}))
    else:
        # If no events found, redirect to events list
        return redirect('user_interactions:events_zh')

def intro_view(request):
    """English intro page - visual-only welcome page"""
    return render(request, 'intro.html')

def intro_view_zh(request):
    """Chinese intro page - visual-only welcome page"""
    return render(request, 'intro_zh.html')