# Register your receivers here
from django.dispatch import receiver

from pretix.base.signals import register_mail_placeholders


@receiver(register_mail_placeholders, dispatch_uid="placeholder_custom")
def register_mail_renderers(sender, **kwargs):
    from .email import OrderAttestationPlaceholder
    return OrderAttestationPlaceholder()
