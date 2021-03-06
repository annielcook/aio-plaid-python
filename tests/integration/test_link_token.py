import time

from tests.integration.util import create_client

import pytest

@pytest.mark.asyncio
async def test_link_token_create_required():
    client = create_client()

    # build the configs
    configs = {
        'user': {
            'client_user_id': str(time.time()),
        },
        'products': ["auth", "transactions"],
        'client_name': "Plaid Test",
    }

    # create link token
    response = await client.LinkToken.create(configs)

    # assert on response
    assert response['link_token'] is not None
    assert response['expiration'] is not None


@pytest.mark.asyncio
async def test_link_token_create_optional():
    client = create_client()

    # build the configs
    configs = {
        'user': {
            'client_user_id': str(time.time()),
        },
        'products': ["auth", "transactions"],
        'client_name': "Plaid Test",
        'country_codes': ['GB'],
        'language': 'en',
        'webhook': 'https://sample-webhook-uri.com',
        'link_customization_name': 'default',
        'account_filters': {
            'depository': {
                'account_subtypes': ['checking', 'savings'],
            },
        },
    }

    # create link token
    response = await client.LinkToken.create(configs)

    # assert on response
    assert response['link_token'] is not None
    assert response['expiration'] is not None
