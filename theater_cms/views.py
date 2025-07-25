from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserFeedback, EmailSubscription, Event, Performance, SeasonalSponsor, EventSponsorImage, SponsorPageContent
from cms.utils import get_current_site
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q

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
    if user_language == 'lt':
        return redirect('/thank-you_lt/')
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
        request.session['subscription_message'] = "You are already subscribed to our newsletter."
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # If valid, save the subscription
    EmailSubscription.objects.create(
        email=email,
        name=name,
        receive_updates=preferences
    )
    
    # Clear any stored errors/data
    if 'subscription_errors' in request.session:
        del request.session['subscription_errors']
    if 'subscription_data' in request.session:
        del request.session['subscription_data']
    
    # Set success message
    request.session['subscription_success'] = True
    
    # Redirect back to the same page to show success message
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def clear_subscription_messages(request):
    """Clear subscription success/message flags from session."""
    if 'subscription_success' in request.session:
        del request.session['subscription_success']
    if 'subscription_message' in request.session:
        del request.session['subscription_message']
    return JsonResponse({'status': 'ok'})

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
    
    # Get sponsor page content
    sponsor_content = SponsorPageContent.get_instance()

    return render(request, 'sponsors.html', {
        'seasonal_sponsors': seasonal_sponsors,
        'event_sponsors': event_sponsors,
        'event': event,
        'sponsor_content': sponsor_content,
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
    if language == 'lt':
        # Redirect to Lithuanian version
        if '/sponsors/' in next_page:
            return redirect('/sponsors_lt/')
        elif '/events/' in next_page:
            return redirect('/events_lt/')
        elif '/feedback/' in next_page:
            return redirect('/feedback_lt/')
        elif '/about/' in next_page:
            return redirect('/about_lt/')
        elif '/email/' in next_page:
            return redirect('/email-subscribe_lt/')
        elif '/qa/' in next_page or '/q&a/' in next_page:
            return redirect('/qa_lt/')
        elif '/home/' in next_page:
            return redirect('/home_lt/')
        else:
            # Default to Lithuanian greeting page
            return redirect('/greeting_lt/')
    else:
        # Redirect to English version (remove _lt suffix)
        if '_lt/' in next_page:
            clean_path = next_page.replace('_lt/', '/', 1)
            if clean_path == '/qa/':
                clean_path = '/q&a/'
            elif clean_path == '/email-subscribe/':
                clean_path = '/email/'
            return redirect(clean_path)
        else:
            return redirect(next_page)

# Language-specific view functions for Lithuanian versions
def greeting_view_lt(request):
    """Lithuanian version of greeting page"""
    request.session['user_language'] = 'lt'
    return render(request, 'greeting_lt.html')

def sponsors_view_lt(request):
    """Lithuanian version of sponsors page"""
    request.session['user_language'] = 'lt'
    seasonal_sponsors = SeasonalSponsor.objects.all()
    event = determine_current_event()
    event_sponsors = []
    if event:
        event_sponsors = event.sponsor_images.all()
    
    # Get sponsor page content
    sponsor_content = SponsorPageContent.get_instance()

    return render(request, 'sponsors_lt.html', {
        'seasonal_sponsors': seasonal_sponsors,
        'event_sponsors': event_sponsors,
        'event': event,
        'sponsor_content': sponsor_content,
        'event_title_lt': event.get_title('lt') if event else None,
    })

def events_view_lt(request):
    """Lithuanian version of events page"""
    request.session['user_language'] = 'lt'
    events = Event.objects.filter(is_active=True).order_by('sort_order', 'start_datetime')
    
    # Add Lithuanian content for each event
    events_with_lt = []
    for event in events:
        event_dict = {
            'event': event,
            'title_lt': event.get_title('lt'),
            'composer_lt': event.get_composer('lt'),
        }
        events_with_lt.append(event_dict)
    
    return render(request, 'events_lt.html', {'events_with_lt': events_with_lt})

def event_detail_lt(request, slug):
    """Lithuanian version of event detail page"""
    request.session['user_language'] = 'lt'
    event = get_object_or_404(Event, slug=slug, is_active=True)
    
    now = timezone.now()
    upcoming_performances = event.performances.filter(start_time__gt=now).order_by('start_time')
    performance_dates = event.performances.dates('start_time', 'day')
    
    # Pre-process Lithuanian content
    context = {
        'event': event,
        'upcoming_performances': upcoming_performances,
        'performance_dates': performance_dates,
        'event_title_lt': event.get_title('lt'),
        'event_composer_lt': event.get_composer('lt'),
        'event_about_content_lt': event.get_about_content('lt'),
        'event_language_lt': event.get_language('lt'),
        'event_conductor_lt': event.get_conductor('lt'),
        'event_director_lt': event.get_director('lt'),
        'event_cast_content_lt': event.get_cast_content('lt'),
        'event_duration_lt': event.get_duration('lt'),
    }
    
    return render(request, 'event_detail_lt.html', context)

def feedback_view_lt(request):
    """Lithuanian version of feedback page"""
    request.session['user_language'] = 'lt'
    return render(request, 'feedback_lt.html')

def about_view_lt(request):
    """Lithuanian version of about page"""
    request.session['user_language'] = 'lt'
    return render(request, 'about_lt.html')

def email_subscribe_lt(request):
    """Lithuanian version of email subscribe page"""
    request.session['user_language'] = 'lt'
    return render(request, 'email_subscribe_lt.html')

def qa_view_lt(request):
    """Lithuanian version of Q&A page"""
    request.session['user_language'] = 'lt'
    return render(request, 'q&a_lt.html')

def thank_you_lt(request):
    """Lithuanian version of thank you page"""
    request.session['user_language'] = 'lt'
    return render(request, 'feedback_thank_you_lt.html')

def home_view_lt(request):
    """Lithuanian version of home page"""
    request.session['user_language'] = 'lt'
    event = determine_current_event()
    
    context = {
        'current_event': event,
    }
    
    # Add Lithuanian-specific variables if there's a current event
    if event:
        context['current_event_title_lt'] = event.get_title('lt')
        context['current_event_composer_lt'] = event.get_composer('lt')
    
    return render(request, 'home_lt.html', context)

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
    return render(request, 'email_subscribe.html')

def qa_view(request):
    """English version of Q&A page"""
    request.session['user_language'] = 'en'
    return render(request, 'q&a.html')

def current_event_lt(request):
    """Redirect to the current event's Lithuanian detail page"""
    event = determine_current_event()
    if event:
        return redirect('user_interactions:event_detail_lt', slug=event.slug)
    else:
        # If no events found, redirect to Lithuanian events list
        return redirect('/events_lt/')
    