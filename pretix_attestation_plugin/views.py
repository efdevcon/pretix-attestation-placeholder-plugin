from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from pretix.control.views.event import EventSettingsViewMixin

from . import forms, models


class PluginSettingsView(EventSettingsViewMixin, FormView):
    form_class = forms.PluginSettingsForm
    template_name = 'pretix_attestation_plugin/attestation_plugin_settings.html'
    permission = 'can_change_event_settings'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            kwargs["current_base_url"] = models.BaseURL.objects.get(event=self.request.event).string_url
        except models.BaseURL.DoesNotExist:
            kwargs["current_base_url"] = "Not set yet"
        return kwargs

    def form_valid(self, form):
        self.write_to_file(form.cleaned_data["keyfile"])
        self.save_base_url(form.cleaned_data["base_url"])
        return super().form_valid(form)

    def write_to_file(self, cleaned_data):
        if(cleaned_data is None):
            return

        upload_data, num_bits = cleaned_data

        try:
            models.KeyFile.objects.update_or_create(
                event=self.request.event,
                defaults={"upload": upload_data}
            )
        except EnvironmentError:
            messages.error(self.request, _('We could not save your changes: Unable to save the file'))
            return

        messages.success(
            self.request,
            _(
                'Successfully uploaded .pem file. '
                'Number of bits {num_bits}'
            ).format(
                num_bits=num_bits
            ),
        )

    def save_base_url(self, base_url):
        if(base_url is None):
            return
        try:
            models.BaseURL.objects.update_or_create(
                event=self.request.event,
                defaults={"string_url": base_url},
            )
        except Exception:
            messages.error(self.request, _('We could not save your changes: Unable to update the url'))
            return

        messages.success(
            self.request,
            _(
                'Successfully changed the base URL '
                'Current base URL is {url}'
            ).format(
                url=base_url
            ),
        )

    def form_invalid(self, form):
        messages.error(self.request, _('We could not save your changes. See below for details.'))
        return super().form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse('plugins:pretix_attestation_plugin:attestation_plugin_settings', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug,
        })
