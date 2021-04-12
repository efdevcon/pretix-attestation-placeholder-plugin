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
