import pytest


@pytest.mark.asyncio
async def test_get(setup_and_teardown_transactions_client):
    access_token, client = setup_and_teardown_transactions_client
    # get all accounts
    response = await client.Accounts.get(access_token)
    assert response['accounts'] is not None

    # get selected accounts
    account_id = response['accounts'][0]['account_id']
    response = await client.Accounts.get(access_token, account_ids=[account_id])
    assert len(response['accounts']) == 1


@pytest.mark.asyncio
async def test_balances_get(setup_and_teardown_transactions_client):
    access_token, client = setup_and_teardown_transactions_client

    # get all accounts
    response = await client.Accounts.balance.get(access_token)
    assert response['accounts'] is not None

    # get selected accounts
    account_id = response['accounts'][0]['account_id']
    response = await client.Accounts.balance.get(
        access_token, account_ids=[account_id])
    assert len(response['accounts']) == 1
