# Register your receivers here
from django.dispatch import receiver

from pretix.base.signals import register_mail_placeholders
from pretix.base.email import SimpleFunctionalMailTextPlaceholder


@receiver(register_mail_placeholders, dispatch_uid="placeholder_custom")
def register_mail_renderers(sender, **kwargs):
    return SimpleFunctionalMailTextPlaceholder(
        'code', ['order'], lambda order: order.code, sample='F8VVL'
    )
