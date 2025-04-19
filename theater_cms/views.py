from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from .models import UserFeedback, EmailSubscription
from cms.utils import get_current_site
from django.views.decorators.http import require_POST

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