import pytest

from plaid import Client
from typing import Tuple, Optional, AsyncGenerator
from tests.integration.util import (
    create_client,
    SANDBOX_INSTITUTION,
    SESSION_MANAGER)


async def setup_and_teardown_client(product: str, webhook: Optional[str] = None) -> AsyncGenerator[str, Client]:
    print('Setup started')
    client = create_client()
    pt_response = await client.Sandbox.public_token.create(
        SANDBOX_INSTITUTION, [product],
        webhook=webhook
    )
    exchange_response = await client.Item.public_token.exchange(
        pt_response['public_token'])
    print('Setup complete')

    access_token = exchange_response['access_token']
    yield access_token, client

    print('Teardown started')
    await client.Item.remove(access_token)
    print('Teardown complete')


@pytest.fixture
async def setup_and_teardown_transactions_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('transactions'):
        return access_token, client


@pytest.fixture
async def setup_and_teardown_assets_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('assets'):
        return access_token, client


@pytest.fixture
async def setup_and_teardown_auth_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('auth'):
        return access_token, client


@pytest.fixture
async def setup_and_teardown_credit_details_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('credit_details'):
        return access_token, client


@pytest.fixture
async def setup_and_teardown_investments_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('investments'):
        return access_token, client


@pytest.fixture
async def setup_and_teardown_transactions_webhook_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('transactions', webhook='https://plaid.com/foo/bar/hook'):
        return access_token, client


@pytest.fixture
async def setup_and_teardown_identity_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('identity'):
        return access_token, client


@pytest.fixture
async def setup_and_teardown_income_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('income'):
        return access_token, client


@pytest.fixture
async def setup_and_teardown_liabilities_client() -> Tuple[str, Client]:
    async for access_token, client in setup_and_teardown_client('liabilities'):
        return access_token, client


@pytest.fixture(autouse=True, scope='function')
async def close_session():
    yield
    if SESSION_MANAGER['session'] is not None and not SESSION_MANAGER['session'].closed:
        print('Closing aio http session!')
        await SESSION_MANAGER['session'].close()
