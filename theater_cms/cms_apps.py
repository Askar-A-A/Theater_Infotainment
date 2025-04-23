from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _   

@apphook_pool.register
class UserInteractionsApphook(CMSApp):
    name = "User Interactions"
    app_name = "user_interactions"  # Match this with urls.py
    
    def get_urls(self, page=None, language=None, **kwargs):
        return ["theater_cms.urls"]

@apphook_pool.register
class TheaterEventsApphook(CMSApp):
    name = "Theater Events"
    app_name = "user_interactions"  # Must match the app_name in your urls.py
    
    def get_urls(self, page=None, language=None, **kwargs):
        return ["theater_cms.urls"]

