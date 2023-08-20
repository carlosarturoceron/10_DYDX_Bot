import os
from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET # gets the HOST info for main and test net
from config import STARK_PRIVATE_KEY_TESTNET, DYDX_API_KEY_TESTNET, DYDX_API_SECRET_TESTNET, DYDX_API_PASSPHRASE_TESTNET
from config import STARK_PRIVATE_KEY_MAINNET, DYDX_API_KEY_MAINNET, DYDX_API_SECRET_MAINNET, DYDX_API_PASSPHRASE_MAINNET

# !!!! SELECT MODE !!!!
MODE = 'dev'

# Close all open positions & orders
ABORT_ALL_POSITIONS = False

# Find Cointegrated pairs
FIND_COINTEGRATED = True # tells the bot to look for new cointegrated pairs

# Place trades
PLACE_TRADES = True # we DO want to go and place trades

# Resolution
RESOLUTION = '1HOUR' # Can be one of 1DAY, 4HOURS, 1HOUR, 30MINS, 15MINS, 5MINS, 1MIN. at https://dydxprotocol.github.io/v3-teacher/#historical-funding

# Sats Window
WINDOW = 21 # when calculating stats we need a rolling window, this is going to use 21

# Thresholds - Opening
MAX_HALF_LIFE = 24 # half life of cointegration, better to keep it low
ZSCORE_THRESH = 1.5 # ZSCORE trigger
USD_PER_TRADE = 50 # amount bet
USD_MIN_COLLATERAL = 1000 # if >= the bot can place orders

# Thresholds - Closing
CLOSE_AT_ZSCORE_CROSS = True
ETHEREUM_ADDRESS = '0x0e20BcE7Ca7dF26e07A015D430E91Bb225bFf756'

# Keys = Export

# Keys development
STARK_PRIVATE_KEY = STARK_PRIVATE_KEY_MAINNET if MODE == 'prod' else STARK_PRIVATE_KEY_TESTNET
DYDX_API_KEY = DYDX_API_KEY_MAINNET if MODE == 'prod' else DYDX_API_KEY_TESTNET
DYDX_API_SECRET = DYDX_API_SECRET_MAINNET if MODE == 'prod' else DYDX_API_SECRET_TESTNET
DYDX_API_PASSPHRASE = DYDX_API_PASSPHRASE_MAINNET if MODE == 'prod' else DYDX_API_PASSPHRASE_TESTNET
HOST = API_HOST_MAINNET if MODE == 'prod' else API_HOST_GOERLI

# HTTP Provider
HTTP_PROVIDER_MAINNET = 'https://eth-mainnet.g.alchemy.com/v2/L8Xvs0EuNzXmCyW1xT1YJ20KicLd1bao'
HTTP_PROVIDER_TESTNET = 'https://eth-goerli.g.alchemy.com/v2/Zdu7kocrSc9qL4PzfcYK4K3E_MXXf9jb'
HTTP_PROVIDER = HTTP_PROVIDER_MAINNET if MODE == 'prod' else HTTP_PROVIDER_TESTNET