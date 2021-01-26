from pretix.base.models import OrderPosition

# Here key indicates .pem file in RFC 5915 format. Before using this generator, key needs
# to be uploaded through form.
# Currently, uploaded keys are stored in KEYFILE_DIR variable specified in views.py. Now
# the directory is "pretix_attestation_plugin/static/pretix_attestation_plugin/keyfiles"


def generate_link(order_position: OrderPosition,
                  path_to_key: str,
                  path_to_generator: str = 'pretix_attestation_plugin/generator/attestation-all.jar',
                  ticket_staus: str = '1') -> str:
    from subprocess import (
        Popen,
        PIPE
    )

    import os.path

    if not os.path.isfile(path_to_key):
        raise ValueError(f'Key file not found in {path_to_key}')

    if not os.path.isfile(path_to_generator):
        raise ValueError(f'Generator file not found in {path_to_generator}')

    email = order_position.attendee_email
    event_id = str(order_position.order.event.id)
    ticket_id = str(order_position.item.id)

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
