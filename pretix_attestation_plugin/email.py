from pretix.base.email import BaseMailTextPlaceholder
from django.utils.translation import gettext_lazy as _

from .models import (
    AttestationLink,
    BaseURL,
)


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
            attestation_text = _("Attestation links does not exist. Please contact the organizers")
            return attestation_text

        for position in context["order"].positions.all():
            try:
                attestation_text += _("Ticket #{id} : {base_url}{link} \n").format(
                    id=position.positionid,
                    base_url=base_url,
                    link=str(AttestationLink.objects.get(order_position=position).string_url)
                )
            except AttestationLink.DoesNotExist:
                attestation_text = _("Attestation links does not exist. Please contact the organizers")
                break

        return attestation_text

    def render_sample(self, event):
        return "http://localhost/?ticket=MIGZMAoCAQYCAgTRA…"
