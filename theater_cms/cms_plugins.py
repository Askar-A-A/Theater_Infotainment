from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import TheaterLogo, SponsorLogo, EventCard
from theater_cms.models import QAItemPlugin

@plugin_pool.register_plugin
class TheaterLogoPlugin(CMSPluginBase):
    model = TheaterLogo
    name = "Theater Logo"
    render_template = "theater_cms/theater_logo.html"
    text_enabled = False
    module = "Theater"

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

@plugin_pool.register_plugin
class SponsorLogoPlugin(CMSPluginBase):
    model = SponsorLogo
    name = "Sponsor Logo"
    render_template = "theater_cms/sponsor_logo.html"
    text_enabled = False
    module = "Theater"

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

@plugin_pool.register_plugin
class EventCardPlugin(CMSPluginBase):
    model = EventCard
    name = "Event Card"
    render_template = "theater_cms/event_card.html"
    text_enabled = False
    module = "Theater"

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

@plugin_pool.register_plugin
class QAItemPluginPublisher(CMSPluginBase):
    model = QAItemPlugin
    name = "Q&A Item"
    render_template = "theater_cms/qa_item.html"
    cache = False
    
    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
