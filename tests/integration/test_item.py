'''
Client.Item.* tests.

Note that when using many of these methods in production, it would be necessary
to handle error cases (e.g. ``INVALID_CREDENTIAL``). However, we don't do that
here since any errors will automatically be marked as failures by the test
runner.
'''
from contextlib import asynccontextmanager

import pytest

from tests.integration.util import (
    create_client,
    SANDBOX_INSTITUTION,
)


@pytest.mark.asyncio
async def test_get(setup_and_teardown_transactions_client):
    access_token, client = setup_and_teardown_transactions_client

    get_response = await client.Item.get(access_token)
    assert get_response['item'] is not None


@pytest.mark.asyncio
async def test_remove(setup_and_teardown_transactions_client):
    access_token, client = setup_and_teardown_transactions_client

    remove_response = await client.Item.remove(access_token)
    assert remove_response['removed']


# Ensure that any items created are also removed
@pytest.mark.asyncio
async def test_public_token():
    client = create_client()
    pt_response = await client.Sandbox.public_token.create(
        SANDBOX_INSTITUTION, ['transactions'])
    exchange_response = await client.Item.public_token.exchange(
        pt_response['public_token'])
    async with ensure_item_removed(exchange_response['access_token']):
        assert pt_response['public_token'] is not None
        assert exchange_response['access_token'] is not None


@asynccontextmanager
async def ensure_item_removed(access_token):
    try:
        yield
    finally:
        await create_client().Item.remove(access_token)


@pytest.mark.asyncio
async def test_sandbox_fire_webhook(setup_and_teardown_transactions_webhook_client):
    access_token, client = setup_and_teardown_transactions_webhook_client

    # fire webhook
    fire_webhook_response = await client.Sandbox.item.fire_webhook(
        access_token,
        'DEFAULT_UPDATE'
    )
    assert fire_webhook_response['webhook_fired'] is True


@pytest.mark.asyncio
async def test_access_token_invalidate():
    client = create_client()
    pt_response = await client.Sandbox.public_token.create(
        SANDBOX_INSTITUTION, ['transactions'])
    exchange_response = await client.Item.public_token.exchange(
        pt_response['public_token'])
    try:
        invalidate_response = await client.Item.access_token.invalidate(
            exchange_response['access_token'])
        async with ensure_item_removed(invalidate_response['new_access_token']):
            assert invalidate_response['new_access_token'] is not None
    except Exception:
        async with ensure_item_removed(exchange_response['access_token']):
            raise


@pytest.mark.asyncio
async def test_webhook_update():
    client = create_client()
    pt_response = await client.Sandbox.public_token.create(
        SANDBOX_INSTITUTION, ['transactions'])
    exchange_response = await client.Item.public_token.exchange(
        pt_response['public_token'])

    async with ensure_item_removed(exchange_response['access_token']):
        webhook_response = await client.Item.webhook.update(
            exchange_response['access_token'],
            'https://plaid.com/webhook-test')
        assert (webhook_response['item']['webhook'] ==
                'https://plaid.com/webhook-test')
