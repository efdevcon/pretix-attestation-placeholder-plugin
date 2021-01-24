from pretix.base.email import BaseMailTextPlaceholder


class OrderAttestationPlaceholder(BaseMailTextPlaceholder):
    def __init__(self):
        self._identifier = "order_attestation_link"

    @property
    def identifier(self):
        return self._identifier

    @property
    def required_context(self):
        return ['event']

    def render(self, context):
        # Change to attestation link
        return "This is Link"

    def render_sample(self, event):
        return "http://localhost/?ticket=MIGZMAoCAQYCAgTRA…"
