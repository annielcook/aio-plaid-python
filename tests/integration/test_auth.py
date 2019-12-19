import pytest


@pytest.mark.asyncio
async def test_get(setup_and_teardown_auth_client):
    access_token, client = setup_and_teardown_auth_client

    # get auth for all accounts
    response = await client.Auth.get(access_token)
    assert response['accounts'] is not None
    assert response['numbers'] is not None

    # get auth for selected accounts
    account_id = response['accounts'][0]['account_id']
    response = await client.Auth.get(access_token, account_ids=[account_id])
    for key in [
        'eft',
        'ach',
        'international',
        'bacs',
    ]:
        assert key in response['numbers']
