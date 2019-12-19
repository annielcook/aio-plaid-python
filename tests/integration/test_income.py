import pytest

from plaid.errors import ItemError


@pytest.mark.asyncio
async def test_get(setup_and_teardown_income_client):
    access_token, client = setup_and_teardown_income_client
    try:
        await client.Income.get(access_token)
    except ItemError as ie:
        assert ie.code == u'PRODUCT_NOT_READY'
