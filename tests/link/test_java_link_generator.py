import pytest

from pretix_attestation_plugin.email import OrderAttestationPlaceholder


@pytest.mark.django_db
def test_link_successfuly_generated(order_position):

    link = OrderAttestationPlaceholder.generate_link(
        email=order_position.attendee_email,
        event_id=str(order_position.order.event.id),
        ticket_id=str(order_position.item.id)
    )

    assert len(link) != 0
    assert link.startswith('?ticket=')


@pytest.mark.django_db
def test_invalid_path_to_key(order_position):
    invalid_path = 'key.pem'

    with pytest.raises(ValueError,
                       match=f'Key file not found in {invalid_path}'):
        OrderAttestationPlaceholder.generate_link(
            email=order_position.attendee_email,
            event_id=str(order_position.order.event.id),
            ticket_id=str(order_position.item.id),
            path_to_key=invalid_path
        )


@pytest.mark.django_db
def test_invalid_path_to_generator(order_position):
    invalid_path = 'generator.jar'

    with pytest.raises(ValueError,
                       match=f'Generator file not found in {invalid_path}'):
        OrderAttestationPlaceholder.generate_link(
            email=order_position.attendee_email,
            event_id=str(order_position.order.event.id),
            ticket_id=str(order_position.item.id),
            path_to_generator=invalid_path
        )
