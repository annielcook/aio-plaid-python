'''Shared objects for integration testing.'''

import os
from typing import Dict, Optional

import aiohttp
from aiohttp import ClientSession

from plaid import Client

SESSION_MANAGER = {
    'session': None
}  # type: Dict[str, Optional[ClientSession]]

def create_client():
    '''Create a new client for testing.'''
    if SESSION_MANAGER['session'] is None or SESSION_MANAGER['session'].closed:
        print('Opening aio http session!')
        SESSION_MANAGER['session'] = aiohttp.ClientSession()
    return Client(os.environ['CLIENT_ID'],
                  os.environ['SECRET'],
                  os.environ['PUBLIC_KEY'],
                  'sandbox',
                  SESSION_MANAGER['session'],
                  api_version="2019-05-29",
                  client_app="plaid-python-unit-tests")


SANDBOX_INSTITUTION = 'ins_109508'
SANDBOX_INSTITUTION_NAME = 'First Platypus Bank'

SANDBOX_INSTITUTIONS = [
    'ins_109508',
    'ins_109509',
    'ins_109510',
    'ins_109511',
    'ins_109512',
]
