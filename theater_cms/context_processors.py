def user_interaction_session_data(request):
    """
    Context processor to make session data available to all templates.
    """
    return {
        # Feedback data
        'feedback_errors': request.session.get('feedback_errors', {}),
        'feedback_data': request.session.get('feedback_data', {}),
        
        # Subscription data
        'subscription_errors': request.session.get('subscription_errors', {}),
        'subscription_data': request.session.get('subscription_data', {}),
        'subscription_success': request.session.get('subscription_success', False),
        'subscription_message': request.session.get('subscription_message', '')
    }

def display_settings(request):
    """Add display height and width to the template context."""
    from .models import SiteSettings
    
    # Get setting from database
    settings = SiteSettings.get_solo()
    
    # Determine width based on height
    width = 1280
    if settings.display_height == 600:
        width = 1024
        
    return {
        'display_height': settings.display_height,
        'display_width': width,
    }
