import re

from OpenSSL import crypto

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from pretix.control.forms import ExtFileField


ADDRESS_RE = re.compile(r"^0x[a-zA-Z0-9]{40}$")
COMMENT_RE = re.compile(r"^#")


class KeyPemFile(ExtFileField):
    def __init__(self, *args, **kwargs):
        kwargs["ext_whitelist"] = (".pem",)
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)

        if data:
            raw_data = data.read()
            try:
                pubkey = crypto.load_privatekey(crypto.FILETYPE_PEM, raw_data)
            except crypto.Error:
                raise forms.ValidationError(_("Unable to load private key"))

            if(pubkey.bits() == 0):
                raise forms.ValidationError(_("Key is 0 bits"))

            return data, pubkey.bits()


class BaseURLField(forms.CharField):
    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)

        if(data):
            validate = URLValidator()

            try:
                validate(data)
            except ValidationError:
                raise forms.ValidationError(_("String is not a valid URL"))

            return data


class PluginSettingsForm(forms.Form):
    def __init__(self, current_base_url="None", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["base_url"] = BaseURLField(
            label=_('Base URL'),
            help_text=_("Type in a Base URL address. Current url: {url}").format(
                url=str(current_base_url)
            ),
            required=False,
        )

    keyfile = KeyPemFile(
        help_text=_("""Upload a '.pem' key file holding a key in RFC 5915 format. <br>
            You can generate it like this: <strong>openssl ecparam -name secp256k1 -genkey -noout -out key.pem</strong>"""),
        required=False,
    )
