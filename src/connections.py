import os
from constants import ETHEREUM_ADDRESS, HOST ,HTTP_PROVIDER, STARK_PRIVATE_KEY, DYDX_API_KEY, DYDX_API_SECRET, DYDX_API_PASSPHRASE
from config import ETH_PRIVATE_KEY

from dydx3 import Client
from web3 import Web3

# Connect to dydx
def connect_dydx():
# Create client connection
    client = Client(
    host= HOST,
    api_key_credentials={
        "key": DYDX_API_KEY,
        "secret": DYDX_API_SECRET,
        "passphrase": DYDX_API_PASSPHRASE
    },
    stark_private_key= STARK_PRIVATE_KEY,
    eth_private_key= ETH_PRIVATE_KEY,
    default_ethereum_address= ETHEREUM_ADDRESS,
    web3= Web3(Web3.HTTPProvider(HTTP_PROVIDER))
    )

    # Confirm client
    account = client.private.get_account()

    return client