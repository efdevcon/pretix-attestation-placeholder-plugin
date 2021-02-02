from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/attestation_plugin_settings/$",
        views.PluginSettingsView.as_view(),
        name="attestation_plugin_settings",
    ),
]
