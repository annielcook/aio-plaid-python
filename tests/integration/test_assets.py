import pytest
import time

from plaid.errors import PlaidError


@pytest.mark.skip(reason='"asset reports with insights" feature is not enabled for your account')
@pytest.mark.asyncio
async def test_full_flow(setup_and_teardown_assets_client):
    access_token, client = setup_and_teardown_assets_client

    # create an asset report for one item
    options = {
        'client_report_id': '123',
        'webhook': 'https://www.example.com',
        'user': {
            'client_user_id': '789',
            'first_name': 'Jane',
            'middle_name': 'Leah',
            'last_name': 'Doe',
            'ssn': '123-45-6789',
            'phone_number': '(555) 123-4567',
            'email': 'jane.doe@example.com',
        }
    }
    response = await client.AssetReport.create(
        [access_token],
        days_requested=60,
        options=options)
    asset_report_token = response['asset_report_token']
    asset_report_id = response['asset_report_id']
    assert asset_report_token is not None
    assert asset_report_id is not None

    # retrieve the asset report
    response = await poll_for_asset_report(client, asset_report_token)
    report = response['report']
    assert report is not None

    # retrieve the asset report as an Asset Report with Insights
    response = await client.AssetReport.get(asset_report_token, True)
    report = response['report']
    assert report is not None

    # The transactions in an Asset Report with Insights should have a non-null
    # `name` (when available).
    assert (
        name_exists_for_some_transaction(report))

    # retrieve the asset report as a PDF
    pdf = await client.AssetReport.get_pdf(asset_report_token)
    assert pdf is not None

    # create a filtered copy of the asset report
    account_ids_to_exclude = [report['items'][0]['accounts'][0]['account_id']]
    response = await client.AssetReport.filter(
        asset_report_token, account_ids_to_exclude)
    assert response['asset_report_token'] is not None

    # create a refreshed copy of the asset report
    response = await client.AssetReport.refresh(asset_report_token, 10)
    assert response['asset_report_token'] is not None

    # create an audit copy
    response = await client.AssetReport.audit_copy.create(
        asset_report_token,
        client.client_id)
    audit_copy_token = response['audit_copy_token']
    assert audit_copy_token is not None

    # get the audit copy
    response = await client.AssetReport.audit_copy.get(audit_copy_token)
    audit_copy = response['report']
    assert audit_copy is not None

    # remove the audit copy token
    response = await client.AssetReport.audit_copy.remove(audit_copy_token)
    removed = response['removed']
    assert removed

    # remove the asset report
    response = await client.AssetReport.remove(asset_report_token)
    removed = response['removed']
    assert removed


def name_exists_for_some_transaction(report):
    for account in report['items'][0]['accounts']:
        if len(account['transactions']) > 0:
            return account['transactions'][0]['name'] is not None

    return False


async def poll_for_asset_report(client, asset_report_token, retries=20):
    try:
        return await client.AssetReport.get(asset_report_token)
    except PlaidError as e:
        if e.code == 'PRODUCT_NOT_READY' and retries > 0:
            time.sleep(1)
            return await poll_for_asset_report(
                client,
                asset_report_token,
                retries - 1)

        raise e
