# Register your receivers here
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _

from pretix.base.signals import register_mail_placeholders
from pretix.base.email import SimpleFunctionalMailTextPlaceholder
from pretix.control.signals import nav_event_settings


@receiver(register_mail_placeholders, dispatch_uid="placeholder_custom")
def register_mail_renderers(sender, **kwargs):
    from .email import OrderAttestationPlaceholder
    return OrderAttestationPlaceholder()


@receiver(nav_event_settings, dispatch_uid='attestation_nav_key_file_upload')
def navbar_key_file_upload(sender, request, **kwargs):
    url = resolve(request.path_info)
    return [{
        'label': _('Key file upload'),
        'url': reverse('plugins:pretix_attestation_plugin:key_file_upload', kwargs={
            'event': request.event.slug,
            'organizer': request.organizer.slug,
        }),
        'active': (
            url.namespace == 'plugins:pretix_attestation_plugin'
            and url.url_name == 'key_file_upload'
        ),
    }]