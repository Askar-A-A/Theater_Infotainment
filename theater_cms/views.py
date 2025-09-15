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
    
    # Comments are now optional - no validation needed
    
    if rating == '0' or not rating:
        errors['rating'] = "Please select a rating."
    elif not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        errors['rating'] = "Please select a valid rating."
    
    # If there are errors, store them in session and redirect back
    if errors:
        # Store errors in the same format as email subscribe (single warning)
        if 'rating' in errors:
            request.session['feedback_warning'] = errors['rating']
        
        request.session['feedback_data'] = {
            'name': name,
            'rating': rating,
            'comments': comments
        }
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # If valid, save the feedback
    rating_int = int(rating)
    
    try:
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
        referrer = request.META.get('HTTP_REFERER', '')
        if '_lt' in referrer or 'lt' in referrer:
            return redirect('user_interactions:thank_you_lt')
        else:
            return redirect('user_interactions:thank_you_page')
            
    except Exception as e:
        # If database save fails, set an error message
        request.session['feedback_errors'] = {'general': 'Failed to save feedback. Please try again.'}
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def thank_you_page(request):
    """
    English thank you page for feedback - uses the regular template
    """
    return render(request, 'feedback_thank_you.html')

def email_thank_you_page(request):
    """
    English thank you page for email subscription
    """
    return render(request, 'email_thank_you.html')

def process_subscription(request):
    """Process email subscription form submissions."""
    # Only process POST requests
    if request.method != 'POST':
        # If accessed directly via GET, redirect back
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    # Extract form data
    email = request.POST.get('email', '').strip().lower()  # Normalize email
    name = request.POST.get('name', '').strip()
    preferences = request.POST.get('preferences', '') == 'on'  # Convert checkbox to boolean
    
    # Validate data
    errors = {}
    
    if not email or '@' not in email or '.' not in email:
        errors['email'] = "Please provide a valid email address."
    
    # If there are errors, store them in session and redirect back
    if errors:
        request.session['subscription_errors'] = errors
        request.session['subscription_data'] = {
            'email': email,
            'name': name,
            'preferences': preferences
        }
        request.session.modified = True
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # Check if email already exists (case-insensitive)
    if EmailSubscription.objects.filter(email__iexact=email).exists():
        # Set language-specific warning message based on the referring page
        referrer = request.META.get('HTTP_REFERER', '')
        if '_lt' in referrer or 'lt' in referrer:
            warning_msg = "Jūs jau esate užsiprenumeravę mūsų naujienlaiškį."
            template_name = 'email_subscribe_lt.html'
        else:
            warning_msg = "You are already subscribed to our newsletter."
            template_name = 'email_subscribe.html'
            
        # Debug logging for WebView troubleshooting
        print(f"SUBSCRIPTION_WARNING: Email {email} already exists")
        print(f"SUBSCRIPTION_WARNING: Referrer: {referrer}")
        print(f"SUBSCRIPTION_WARNING: Warning message: {warning_msg}")
        
        # Render template directly with warning context (no session, no redirect)
        context = {
            'subscription_warning': warning_msg,
            'subscription_data': {
                'email': email,
                'name': name,
                'preferences': preferences
            }
        }
        return render(request, template_name, context)
    
    # If valid, save the subscription with error handling
    try:
        subscription = EmailSubscription.objects.create(
            email=email,
            name=name,
            receive_updates=preferences
        )
        
        # Debug logging for successful subscription
        print(f"SUBSCRIPTION_SUCCESS: Created subscription for {email}")
        print(f"SUBSCRIPTION_SUCCESS: ID: {subscription.id}, Name: {name}, Preferences: {preferences}")
        
        # Clear any stored errors/data/warnings
        session_keys_to_clear = [
            'subscription_errors', 
            'subscription_data', 
            'subscription_warning'
        ]
        for key in session_keys_to_clear:
            if key in request.session:
                del request.session[key]
        
        # Redirect to appropriate thank you page based on language
        referrer = request.META.get('HTTP_REFERER', '')
        if '_lt' in referrer or 'lt' in referrer:
            return redirect('user_interactions:email_thank_you_lt')
        else:
            return redirect('user_interactions:email_thank_you_page')
        
    except Exception as e:
        # Handle database errors
        print(f"SUBSCRIPTION_ERROR: Failed to create subscription for {email}: {str(e)}")
        request.session['subscription_errors'] = {'email': 'Failed to save subscription. Please try again.'}
        request.session['subscription_data'] = {
            'email': email,
            'name': name,
            'preferences': preferences
        }
        request.session.modified = True
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def clear_subscription_messages(request):
    """Clear subscription success/message flags from session."""
    try:
        # Clear only subscription-related session data
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

@require_POST
def clear_feedback_messages(request):
    """Clear feedback error/message flags from session."""
    try:
        # Clear only feedback-related session data
        session_keys_to_clear = [
            'feedback_errors',
            'feedback_data',
            'feedback_warning'  # Add this
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
            'message': 'Feedback messages cleared successfully'
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

# Language switching is handled through direct URL routing
# English URLs: /sponsors/, /events/, etc.
# Lithuanian URLs: /sponsors_lt/, /events_lt/, etc.
# Templates contain direct links to switch between languages

# Language-specific view functions for Lithuanian versions
def greeting_view_lt(request):
    """Lithuanian version of greeting page"""
    return render(request, 'greeting_lt.html')

def sponsors_view_lt(request):
    """Lithuanian version of sponsors page"""
    seasonal_sponsors = SeasonalSponsor.objects.all()
    event = determine_current_event()
    event_sponsors = []
    if event:
        event_sponsors = event.sponsor_images.all()
    
    # Get sponsors page content
    sponsors_content = SponsorsPageContent.get_content()

    return render(request, 'sponsors_lt.html', {
        'seasonal_sponsors': seasonal_sponsors,
        'event_sponsors': event_sponsors,
        'event': event,
        'sponsors_content': sponsors_content,
    })

def events_view_lt(request):
    """Lithuanian version of events page"""
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
        'event_about_lt': event.get_about_content('lt'),
        'event_language_lt': event.get_language('lt'),
        'event_conductor_lt': event.get_conductor('lt'),
        'event_director_lt': event.get_director('lt'),
        'event_cast_lt': event.get_cast_content('lt'),
        'event_duration_lt': event.get_duration('lt'),
    }
    
    return render(request, 'event_detail_lt.html', context)

def feedback_view_lt(request):
    """Lithuanian version of feedback page"""
    
    # Clear old error messages if user navigates back to feedback page
    # This provides a fallback if JavaScript clearing fails
    if not request.session.get('feedback_success') and not request.session.get('feedback_success_message'):
        # Only clear if there are no active success messages to display
        session_keys_to_clear = ['feedback_errors', 'feedback_data']
        for key in session_keys_to_clear:
            if key in request.session:
                del request.session[key]
    
    return render(request, 'feedback_lt.html')

def about_view_lt(request):
    """Lithuanian version of about page"""
    return render(request, 'about_lt.html')

def email_subscribe_lt(request):
    """Lithuanian version of email subscribe page"""
    
    # Clear old messages if user navigates back to subscription page
    # This provides a fallback if JavaScript clearing fails
    if not request.session.get('subscription_success') and not request.session.get('subscription_message'):
        # Only clear if there are no active messages to display
        session_keys_to_clear = ['subscription_errors', 'subscription_data']
        for key in session_keys_to_clear:
            if key in request.session:
                del request.session[key]
    
    return render(request, 'email_subscribe_lt.html')

def qa_view_lt(request):
    """Lithuanian version of Q&A page"""
    return render(request, 'q&a_lt.html')

def thank_you_lt(request):
    """Lithuanian version of thank you page for feedback"""
    return render(request, 'feedback_thank_you_lt.html')

def email_thank_you_lt(request):
    """Lithuanian version of thank you page for email subscription"""
    return render(request, 'email_thank_you_lt.html')

def home_view_lt(request):
    """Lithuanian version of home page"""
    event = determine_current_event()
    return render(request, 'home_lt.html', {'current_event': event})

def home_view(request):
    """English version of home page"""
    event = determine_current_event()
    return render(request, 'home.html', {'current_event': event})

def feedback_view(request):
    """English version of feedback page"""
    
    # Clear old error messages if user navigates back to feedback page
    # This provides a fallback if JavaScript clearing fails
    if not request.session.get('feedback_success') and not request.session.get('feedback_success_message'):
        # Only clear if there are no active success messages to display
        session_keys_to_clear = ['feedback_errors', 'feedback_data']
        for key in session_keys_to_clear:
            if key in request.session:
                del request.session[key]
    
    return render(request, 'feedback.html')

def about_view(request):
    """English version of about page"""
    return render(request, 'about.html')

def email_subscribe(request):
    """English version of email subscribe page"""
    
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
    return render(request, 'q&a.html')

def current_event_lt(request):
    """Redirect to the current event's detail page (Lithuanian)"""
    event = determine_current_event()
    if event:
        return redirect(reverse('user_interactions:event_detail_lt', kwargs={'slug': event.slug}))
    else:
        # If no events found, redirect to events list
        return redirect('user_interactions:events_lt')

def intro_view(request):
    """English intro page - visual-only welcome page"""
    return render(request, 'intro.html')

def intro_view_lt(request):
    """Lithuanian intro page - visual-only welcome page"""
    return render(request, 'intro_lt.html')