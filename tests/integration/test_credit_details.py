import pytest


@pytest.mark.asyncio
async def test_get(setup_and_teardown_credit_details_client):
    access_token, client = setup_and_teardown_credit_details_client
    response = await client.CreditDetails.get(access_token)
    assert response['accounts'] is not None
    assert response['credit_details'] is not None
