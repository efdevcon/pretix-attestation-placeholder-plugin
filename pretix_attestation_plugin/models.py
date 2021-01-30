from django.db import (
    models,
)
from pretix.base.models import (
    Event,
)


class BaseURL(models.Model):
    """
    Represents a base url used for generating a attestation link
    """
    string_url = models.CharField(max_length=4096)

    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True
    )
