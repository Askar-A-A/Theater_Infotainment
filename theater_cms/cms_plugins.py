from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import TheaterLogo, SponsorLogo, EventCard

@plugin_pool.register_plugin
class TheaterLogoPlugin(CMSPluginBase):
    model = TheaterLogo
    name = _("Theater Logo")
    render_template = "theater_cms/theater_logo.html"
    text_enabled = False
    module = _("Theater")

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

@plugin_pool.register_plugin
class SponsorLogoPlugin(CMSPluginBase):
    model = SponsorLogo
    name = _("Sponsor Logo")
    render_template = "theater_cms/sponsor_logo.html"
    text_enabled = False
    module = _("Theater")

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

@plugin_pool.register_plugin
class EventCardPlugin(CMSPluginBase):
    model = EventCard
    name = _("Event Card")
    render_template = "theater_cms/event_card.html"
    text_enabled = False
    module = _("Theater")

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context
