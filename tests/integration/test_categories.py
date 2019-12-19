import pytest
from tests.integration.util import (
    create_client,
)


@pytest.mark.asyncio
async def test_get():
    client = create_client()
    response = await client.Categories.get()
    assert response['categories'] is not None
