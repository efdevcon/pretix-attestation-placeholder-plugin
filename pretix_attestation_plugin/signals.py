# Register your receivers here
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
import logging

from pretix.base.signals import (
    register_mail_placeholders,
)
from pretix.control.signals import nav_event_settings


logger = logging.getLogger(__name__)


@receiver(register_mail_placeholders, dispatch_uid="placeholder_custom")
def register_mail_renderers(sender, **kwargs):
    from .email import OrderAttestationPlaceholder, PositionAttestationPlaceholder
    return [OrderAttestationPlaceholder(), PositionAttestationPlaceholder()]


@receiver(nav_event_settings, dispatch_uid='attestation_nav_key_file_upload')
def navbar_key_file_upload(sender, request, **kwargs):
    url = resolve(request.path_info)
    return [{
        'label': _('Attestation Plugin Settings'),
        'url': reverse('plugins:pretix_attestation_plugin:attestation_plugin_settings', kwargs={
            'event': request.event.slug,
            'organizer': request.organizer.slug,
        }),
        'active': (
            url.namespace == 'plugins:pretix_attestation_plugin'
            and url.url_name == 'attestation_plugin_settings'
        ),
    }]
