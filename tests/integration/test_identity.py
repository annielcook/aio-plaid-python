import pytest


@pytest.mark.asyncio
async def test_get(setup_and_teardown_identity_client):
    access_token, client = setup_and_teardown_identity_client
    response = await client.Identity.get(access_token)
    assert response['accounts'] is not None
    for account in response['accounts']:
        assert account['owners'] is not None
        assert len(account['owners']) > 0
