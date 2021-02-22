from pretix.base.email import BaseMailTextPlaceholder

from .models import AttestationLink


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
        attestation_link = ""
        for position in context["order"].positions.all():
            try:
                attestation_link += str(AttestationLink.objects.get(order_position=position).string_url) + "\n"
            except AttestationLink.DoesNotExist:
                attestation_link = "Attestation link does not exist. Please contact the organizers"
                break

        return attestation_link

    def render_sample(self, event):
        return "http://localhost/?ticket=MIGZMAoCAQYCAgTRA…"
