# Register your receivers here
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _

from pretix.base.signals import (
    order_placed,
    register_mail_placeholders,
)
from pretix.control.signals import nav_event_settings

from .models import OrderPosition
from .views import KEYFILE_DIR

@receiver(register_mail_placeholders, dispatch_uid="placeholder_custom")
def register_mail_renderers(sender, **kwargs):
    from .email import OrderAttestationPlaceholder
    return OrderAttestationPlaceholder()


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
        # TODO call generate_link(OrderPosition, path_to_key)

        # Temporary link
        link = "{path}/temp_link".format(
            path=path_to_key,
        )

        # Save the link to DB
        OrderPosition.objects.update_or_create(
            order_position=position,
            defaults={"string_url": link},
        )
