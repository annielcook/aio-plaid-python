import pytest


@pytest.mark.asyncio
async def test_get(setup_and_teardown_investments_client):
    access_token, client = setup_and_teardown_investments_client
    response = await client.Holdings.get(access_token)
    assert response['item'] is not None
    assert response['accounts'] is not None
    assert response['securities'] is not None
    assert response['holdings'] is not None
