from django.utils.deprecation import MiddlewareMixin

class DisplayHeightMiddleware(MiddlewareMixin):
    """Middleware to set the display height cookie based on admin settings."""
    
    def process_response(self, request, response):
        from .models import SiteSettings
        
        # Get current height from settings
        settings = SiteSettings.get_solo()
        current_height = str(settings.display_height)
        
        # Set width based on height
        width = "1280"
        if current_height == "600":
            width = "1024"
        
        # Only set cookie if it's missing or different
        if request.COOKIES.get('displayHeight') != current_height:
            # Set cookie for 30 days
            response.set_cookie(
                'displayHeight',
                current_height,
                max_age=30*24*60*60,  # 30 days
                path='/'
            )
        
        # Set width cookie if needed
        if request.COOKIES.get('displayWidth') != width:
            response.set_cookie(
                'displayWidth',
                width,
                max_age=30*24*60*60,  # 30 days
                path='/'
            )
            
        return response 