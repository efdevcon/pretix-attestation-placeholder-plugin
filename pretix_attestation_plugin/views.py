from datetime import timedelta

from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import NaturalTimeFormatter
from django.core.signing import BadSignature, TimestampSigner
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from pretix.control.views.event import EventSettingsViewMixin

from . import forms


UPLOAD_ADDRESS_KEY = "pretix_eth_upload_addresses"
UPLOAD_VALID_DURATION = timedelta(minutes=5)


class KeyFileUploadView(EventSettingsViewMixin, FormView):
    form_class = forms.KeyFileUploadForm
    template_name = 'pretix_attestation_plugin/key_file_upload.html'
    permission = 'can_change_event_settings'

    def form_valid(self, form):
        raw_data, num_bits = form.cleaned_data["key_file_data"]

        messages.success(
            self.request,
            _(
                'Successfully uploaded .pem file. '
                'Public key is {n} bits'
            ).format(
                n=num_bits,
            ),
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('We could not save your changes. See below for details.'))
        return super().form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse('plugins:pretix_attestation_plugin:key_file_upload', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug,
        })