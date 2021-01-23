from pretix.base.email import BaseMailTextPlaceholder


class OrderAttestationPlaceholder(BaseMailTextPlaceholder):
    def __init__(self):
        self._identifier = "attestation_link"

    @property
    def identifier(self):
        return self._identifier

    @property
    def required_context(self):
        return ['event']

    def render(self, context):
        # Change to attestation link
        return "This is Link"

    def render_sample(self, event):
        return "http://localhost/?ticket=MIGZMAoCAQYCAgTRA…"

    @staticmethod
    def generate_link(email: str,
                       event_id: str,
                       ticket_id: str,
                       path_to_key='pretix_attestation_plugin/generator/key.pem',
                       path_to_generator='pretix_attestation_plugin/generator/attestation-all.jar',
                       ticket_staus='1') -> str:
        from subprocess import (
            Popen,
            PIPE
        )

        import os.path

        if not os.path.isfile(path_to_key):
            raise ValueError(f'Key file not found in {path_to_key}')

        if not os.path.isfile(path_to_generator):
            raise ValueError(f'Generator file not found in {path_to_generator}')

        process = Popen(['java', '-cp', path_to_generator,
                         'org.devcon.ticket.Issuer',
                         path_to_key, email, event_id, ticket_id, ticket_staus],
                        stdout=PIPE, stderr=PIPE)

        process.wait()

        error_message = process.stderr.read()
        if (error_message != b''):
            raise ValueError(f'Error message recieved: {error_message}')

        output = process.stdout.read().decode('utf-8')

        return output
