from os import path
from subprocess import Popen, PIPE

from pretix.base.models import OrderPosition

"""
A key indicates .pem file in RFC 5915 format.

Before using this generator, key needs to be uploaded through form.
`Attestation Plugin Settings` can be used for that.
"""


def generate_link(order_position: OrderPosition,
                  path_to_key: str,
                  generator_jar: str = 'attestation-all.jar',
                  ticket_staus: str = '1') -> str:

    if not path.isfile(path_to_key):
        raise ValueError(f'Key file not found in {path_to_key}')

    # either generator_jar is the full path to the java file or it sits next to the python file
    if path.isfile(generator_jar):
        path_to_generator = path.abspath(generator_jar)
    else:
        this_module_path = path.dirname(path.abspath(__file__))
        path_to_generator = path.join(this_module_path, generator_jar)
    if not path.isfile(path_to_generator):
        raise ValueError(f'Generator file not found in {generator_jar}')

    email = order_position.attendee_email
    event_id = str(order_position.order.event.id)
    ticket_id = str(order_position.order.id)

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
