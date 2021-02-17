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
        return ['event', 'position']

    def render(self, context):
        # Change to attestation link
        return str(AttestationLink.objects.get(order_position=context.position).string_url)

    def render_sample(self, event):
        return "http://localhost/?ticket=MIGZMAoCAQYCAgTRA…"
