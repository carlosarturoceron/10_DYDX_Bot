import os
from dotenv import load_dotenv
import sys

# Assuming your .env file is located in the parent directory
dotenv_path = os.path.join(os.path.dirname(sys.path[0]), '.env')
load_dotenv(dotenv_path)

# Retrieve values from environment variables
wallet_dict = os.getenv("wallet_dict")
api_dict = os.getenv("api_dict")


# ENV FILES DO NOT STORE DICTIONARIES !!!!
key = os.getenv('key')
walletAddress = os.getenv('walletAddress')
secret = os.getenv('secret')
passphrase = os.getenv('passphrase')
legacySigning = os.getenv('legacySigning')
walletType = os.getenv('walletType')
publicKey = os.getenv('publicKey')
publicKeyYCoordinate = os.getenv('publicKeyYCoordinate')
privateKey = os.getenv('privateKey')

# ETH Private Key
ETH_PRIVATE_KEY = os.getenv('ETH_PRIVATE_KEY')

# Keys development
STARK_PRIVATE_KEY_TESTNET = os.getenv('STARK_PRIVATE_KEY_TESTNET')
DYDX_API_KEY_TESTNET = os.getenv('DYDX_API_KEY_TESTNET')
DYDX_API_SECRET_TESTNET = os.getenv('DYDX_API_SECRET_TESTNET')
DYDX_API_PASSPHRASE_TESTNET = os.getenv('DYDX_API_PASSPHRASE_TESTNET')

# key, walletAddress, secret, passphrase, legacySigning, walletType, publicKey, publicKeyYCoordinate, privateKey)
STARK_PRIVATE_KEY_MAINNET = os.getenv('STARK_PRIVATE_KEY_MAINNET')
DYDX_API_KEY_MAINNET = os.getenv('DYDX_API_KEY_MAINNET')
DYDX_API_SECRET_MAINNET = os.getenv('DYDX_API_SECRET_MAINNET')
DYDX_API_PASSPHRASE_MAINNET = os.getenv('DYDX_API_PASSPHRASE_MAINNET')