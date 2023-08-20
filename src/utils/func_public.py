from constants import RESOLUTION
from utils.utils import get_ISO_times
from pprint import pprint # to pring pretty

# To wrangle data
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
# Ger relevant time periods for ISO from and to
ISO_TIMES = get_ISO_times()
pprint(ISO_TIMES)

# Construct market prices 
def construct_market_prices(client):
    pass