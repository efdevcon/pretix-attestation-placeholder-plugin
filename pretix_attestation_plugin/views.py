from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from pretix.control.views.event import EventSettingsViewMixin

from . import forms


KEYFILE_DIR = "pretix_attestation_plugin/static/pretix_attestation_plugin/keyfiles"


class KeyFileUploadView(EventSettingsViewMixin, FormView):
    form_class = forms.KeyFileUploadForm
    template_name = 'pretix_attestation_plugin/key_file_upload.html'
    permission = 'can_change_event_settings'

    def form_valid(self, form):
        raw_data, num_bits = form.cleaned_data["key_file_data"]

        file_name = "{dir}/{event}_key.pem".format(
            dir=KEYFILE_DIR,
            event=self.request.event
        )

        try:
            with open(file_name, 'wb') as f:
                f.write(raw_data)
        except EnvironmentError:
            messages.error(self.request, _('We could not save your changes. Unable to save the file'))
            return super().form_valid(form)

        messages.success(
            self.request,
            _(
                'Successfully uploaded .pem file. '
                'Public key is {n} bits'
            ).format(
                n=num_bits
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
