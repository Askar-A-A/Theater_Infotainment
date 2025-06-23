# Middleware removed - no longer needed for fixed 1024x600 resolution
# The display height and width are now handled by the context processor with fixed values 

class DisableCOOPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Remove problematic headers for development
        if hasattr(response, 'headers'):
            response.headers.pop('Cross-Origin-Opener-Policy', None)
            response.headers.pop('Cross-Origin-Embedder-Policy', None)
        return response 