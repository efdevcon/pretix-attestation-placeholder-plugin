import pytest

from pretix_attestation_plugin.generator.java_generator_wrapper import generate_link


@pytest.mark.django_db
def test_link_successfuly_generated(order_position):

    link = generate_link(
        order_position=order_position,
        path_to_key='tests/key.pem'
    )

    assert len(link) != 0
    assert link.startswith('?ticket=')


@pytest.mark.django_db
def test_invalid_path_to_key(order_position):
    invalid_path = 'key.pem'

    with pytest.raises(ValueError,
                       match=f'Key file not found in {invalid_path}'):
        generate_link(
            order_position=order_position,
            path_to_key=invalid_path
        )


@pytest.mark.django_db
def test_invalid_path_to_generator(order_position):
    invalid_path = 'generator.jar'

    with pytest.raises(ValueError,
                       match=f'Generator file not found in {invalid_path}'):
        generate_link(
            order_position=order_position,
            path_to_key='tests/key.pem',
            path_to_generator=invalid_path
        )
