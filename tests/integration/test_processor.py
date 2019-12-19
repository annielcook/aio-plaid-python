'''
Client.Processor.* tests.
'''
import pytest

from plaid.errors import InvalidRequestError

from tests.integration.util import (
    create_client
)


@pytest.mark.asyncio
async def test_stripe_processor_token():
    client = create_client()
    # Just test the failure case - behavior here depends on the API keys used
    with pytest.raises(InvalidRequestError) as e:
        await client.Processor.stripeBankAccountTokenCreate(
            'fakeAccessToken', 'fakeAccountId')
        assert e.code == 'INVALID_INPUT'


@pytest.mark.asyncio
async def test_dwolla_processor_token():
    client = create_client()
    # Just test the failure case - behavior here depends on the API keys used
    with pytest.raises(InvalidRequestError) as e:
        await client.Processor.dwollaBankAccountTokenCreate(
            'fakeAccessToken', 'fakeAccountId')
        assert e.code == 'INVALID_INPUT'
