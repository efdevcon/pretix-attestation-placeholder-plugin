import pytest
import datetime
import contextlib
import pretix

from packaging import version
from decimal import Decimal
from django.utils import timezone

from pretix.base.models import (
    Event,
    Organizer,
    OrderPayment,
    Order,
    OrderPosition,
)
from pytest_django.fixtures import (
    _disable_native_migrations,
)

from django.test import utils
from django_scopes import scopes_disabled

# Disabled scope for databases, otherwise django_scopes breaks
# Django test runner
# Source: https://github.com/raphaelm/django-scopes#testing
utils.setup_databases = scopes_disabled()(utils.setup_databases)


@pytest.fixture
def organizer():
    return Organizer.objects.create(
        name='Ethereum Foundation',
        slug='ef',
    )


@pytest.fixture
def event(organizer):
    now = timezone.now()

    presale_start_at = now + datetime.timedelta(days=2)
    presale_end_at = now + datetime.timedelta(days=6)
    start_at = now + datetime.timedelta(days=7)
    end_at = now + datetime.timedelta(days=14)

    event = Event.objects.create(
        name='Devcon',
        slug='devcon',
        organizer=organizer,
        date_from=start_at,
        date_to=end_at,
        presale_start=presale_start_at,
        presale_end=presale_end_at,
        location='Osaka',
        plugins='pretix_eth',
    )

    return event


@pytest.fixture
def ticket(event, get_organizer_scope):
    with get_organizer_scope():
        return event.items.create(name='Ticket', default_price=Decimal('10.00'))


@pytest.fixture
def get_organizer_scope(organizer):
    if version.parse(pretix.__version__) >= version.parse('3.0.0'):
        # If pretix>=3.0.0, we must scope certain database queries explicitly
        from django_scopes import scope

        return lambda: scope(organizer=organizer)
    else:
        # Otherwise, the scope manager is just a no-op
        @contextlib.contextmanager
        def noop_scope():
            yield

        return noop_scope


@pytest.fixture
def get_order_and_payment(django_db_reset_sequences, event, get_organizer_scope):
    def _get_order_and_payment(order_kwargs=None, payment_kwargs=None, info_data=None):
        with get_organizer_scope():
            # Create order
            final_order_kwargs = {
                'event': event,
                'email': 'test@example.com',
                'locale': 'en_US',
                'datetime': timezone.now(),
                'total': Decimal('100.00'),
                'status': Order.STATUS_PENDING,
            }
            if order_kwargs is not None:
                final_order_kwargs.update(order_kwargs)
            order = Order.objects.create(**final_order_kwargs)

            # Create payment
            final_payment_kwargs = {
                'amount': '100.00',
                'state': OrderPayment.PAYMENT_STATE_PENDING,
            }
            if payment_kwargs is not None:
                final_payment_kwargs.update(payment_kwargs)
            final_payment_kwargs['order'] = order
            payment = OrderPayment.objects.create(**final_payment_kwargs)

            # Add payment json data if provided
            if info_data is not None:
                payment.info_data = info_data
                payment.save(update_fields=['info'])

        return order, payment

    return _get_order_and_payment


@pytest.fixture
def order_position(django_db_reset_sequences, ticket, get_order_and_payment, get_organizer_scope):
    order, payment = get_order_and_payment()

    with get_organizer_scope():
        order_position = OrderPosition.objects.create(
            order=order,
            item=ticket,
            variation=None,
            price=payment.amount,
            attendee_email=order.email
        )

        return order_position


@pytest.fixture(scope="function")
def django_db_setup(
    request,
    django_test_environment,
    django_db_blocker,
    django_db_use_migrations,
    django_db_keepdb,
    django_db_createdb,
    django_db_modify_db_settings,
):
    """
    Copied and pasted from here:
    https://github.com/pytest-dev/pytest-django/blob/d2973e21c34d843115acdbccdd7a16cb2714f4d3/pytest_django/fixtures.py#L84
    """
    from pytest_django.compat import setup_databases, teardown_databases

    setup_databases_args = {}

    if not django_db_use_migrations:
        _disable_native_migrations()

    if django_db_keepdb and not django_db_createdb:
        setup_databases_args["keepdb"] = True

    with django_db_blocker.unblock():
        db_cfg = setup_databases(
            verbosity=request.config.option.verbose,
            interactive=False,
            **setup_databases_args
        )

    def teardown_database():
        with django_db_blocker.unblock():
            try:
                teardown_databases(db_cfg, verbosity=request.config.option.verbose)
            except Exception as exc:
                request.node.warn(
                    pytest.PytestWarning(
                        "Error when trying to teardown test databases: %r" % exc
                    )
                )

    if not django_db_keepdb:
        request.addfinalizer(teardown_database)
