import re

from OpenSSL import crypto

from django import forms
from django.utils.translation import ugettext_lazy as _
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

            return raw_data, pubkey.bits()


class KeyFileUploadForm(forms.Form):
    key_file_data = KeyPemFile(
        help_text=_("""Upload a '.pem' key file holding a key in RFC 5915 format. <br>
            You can generate it like this: <strong>openssl ecparam -name secp256k1 -genkey -noout -out key.pem</strong>"""),
    )
