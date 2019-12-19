import pytest


@pytest.mark.asyncio
async def test_get(setup_and_teardown_liabilities_client):
    access_token, client = setup_and_teardown_liabilities_client
    response = await client.Liabilities.get(access_token)
    assert response['item'] is not None
    assert response['accounts'] is not None
    assert response['liabilities'] is not None

    # get liabiliteis for specified account
    account_id = response['accounts'][0]['account_id']
    response = await client.Liabilities.get(access_token,
                                            account_ids=[account_id])
    assert response['liabilities'] is not None
    assert len(response['accounts']) == 1
