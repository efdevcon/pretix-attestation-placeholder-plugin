from pretix.base.email import BaseMailTextPlaceholder
from django.utils.translation import gettext_lazy as _

from .generator.java_generator_wrapper import generate_link

from .models import (
    AttestationLink,
    BaseURL,
    KeyFile,
)

"""
We need to register two email placeholders under the same name,
the proper one is picked based on the different context.
"""


class OrderAttestationPlaceholder(BaseMailTextPlaceholder):
    def __init__(self):
        self._identifier = "attestation_link"

    @property
    def identifier(self):
        return self._identifier

    @property
    def required_context(self):
        return ['event', 'order']

    def render(self, context):
        # Change to attestation link
        attestation_text = ""
        base_url = ""
        try:
            base_url = BaseURL.objects.get(event=context["event"]).string_url
        except BaseURL.DoesNotExist:
            attestation_text = _("Could not generate attestation URL - please contact support@devcon.org")
            return attestation_text

        order = context['order']

        try:
            path_to_key = KeyFile.objects.get(event=order.event).upload.path
        except KeyFile.DoesNotExist:
            attestation_text = _("Could not generate attestation URL - please contact support@devcon.org")
            return attestation_text

        for position in order.positions.all():
            if position.attendee_email == order.email:
                if not AttestationLink.objects.filter(order_position=position).exists():
                    try:
                        link = generate_link(position, path_to_key)
                    except ValueError:
                        attestation_text = _("Could not generate attestation URL - please contact support@devcon.org")
                        continue
                    AttestationLink.objects.update_or_create(
                        order_position=position,
                        defaults={"string_url": link},
                    )
                try:
                    attestation_text = "{base_url}{link}".format(
                        base_url=base_url,
                        link=str(AttestationLink.objects.get(order_position=position).string_url)
                    )
                except AttestationLink.DoesNotExist:
                    attestation_text = _("Could not generate attestation URL - please contact support@devcon.org")

        return attestation_text

    def render_sample(self, event):
        return "http://localhost/?ticket=MIGZMAoCAQYCAgTRA…"


class PositionAttestationPlaceholder(BaseMailTextPlaceholder):
    def __init__(self):
        self._identifier = "attestation_link"

    @property
    def identifier(self):
        return self._identifier

    @property
    def required_context(self):
        return ['event', 'position']

    def render(self, context):
        # Change to attestation link
        attestation_text = ""
        base_url = ""
        try:
            base_url = BaseURL.objects.get(event=context["event"]).string_url
        except BaseURL.DoesNotExist:
            attestation_text = _("Could not generate attestation URL - please contact support@devcon.org")
            return attestation_text

        position = context["position"]
        event = context["event"]
        
        try:
            path_to_key = KeyFile.objects.get(event=event).upload.path
        except KeyFile.DoesNotExist:
            attestation_text = _("Could not generate attestation URL - please contact support@devcon.org")
            return attestation_text

        if not AttestationLink.objects.filter(order_position=position).exists():
            try:
                link = generate_link(position, path_to_key)
            except ValueError:
                attestation_text = _("Could not generate attestation URL - please contact support@devcon.org")
                return attestation_text
            AttestationLink.objects.update_or_create(
                order_position=position,
                defaults={"string_url": link},
            )

        try:
            attestation_text = "{base_url}{link}".format(
                base_url=base_url,
                link=str(AttestationLink.objects.get(order_position=position).string_url)
            )
        except AttestationLink.DoesNotExist:
            attestation_text = _("Could not generate attestation URL - please contact support@devcon.org")

        return attestation_text

    def render_sample(self, event):
        return "http://localhost/?ticket=MIGZMAoCAQYCAgTRA…"
