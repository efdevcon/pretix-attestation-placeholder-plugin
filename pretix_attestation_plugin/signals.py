# Register your receivers here
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
import logging

from pretix.base.signals import (
    order_placed,
    register_mail_placeholders,
)
from pretix.control.signals import nav_event_settings

from .generator.java_generator_wrapper import generate_link
from .models import AttestationLink
from .views import KEYFILE_DIR


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


@receiver(order_placed, dispatch_uid='attestation_order_placed')
def register_order_placed(order, sender, ** kwargs):

    path_to_key = "{dir}/{event}_key.pem".format(
        dir=KEYFILE_DIR,
        event=str(order.event),
    )

    for position in order.positions.all():
        # generated link
        try:
            link = generate_link(position, path_to_key)
        except ValueError as error:
            logger.error(error)
            continue
        # Save the link to DB
        AttestationLink.objects.update_or_create(
            order_position=position,
            defaults={"string_url": link},
        )
