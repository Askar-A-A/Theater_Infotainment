from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserFeedback, EmailSubscription, Event, Performance
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
    
    # Redirect to thank you page
    return HttpResponseRedirect(reverse('user_interactions:thank_you'))

def thank_you_page(request):
    """
    Render the thank you page.
    This does render a template because it's a dedicated view, not a CMS page.
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