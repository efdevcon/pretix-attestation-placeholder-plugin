from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = '0.2.1'


class PluginApp(PluginConfig):
    name = 'pretix_attestation_plugin'
    verbose_name = 'Pretix Attestation Placeholder Plugin'

    class PretixPluginMeta:
        name = gettext_lazy('Pretix Attestation Placeholder Plugin')
        author = 'Pretix Ethereum Plugin Developers'
        description = gettext_lazy('Pretix Ethereum Plugin Developers')
        visible = True
        version = __version__
        category = 'Other'
        compatibility = "pretix>=3.8.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_attestation_plugin.PluginApp'
