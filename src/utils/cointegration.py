# Data Wrangling
import pandas as pd
import numpy as np
from pprint import pprint # pretty print

# Stats
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

# MAX_HALFLIFE, WINDOW
from constants import MAX_HALF_LIFE, WINDOW

#Calculate Halflife
def calculate_halflife(spread):
    df_spread = pd.DataFrame(spread, columns=['spread'])
    spread_lag = df_spread['spread'].shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_ret = df_spread['spread'] - spread_lag
    spread_ret.iloc[0] = spread_ret.iloc[1]
    spread_lag_2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_ret, spread_lag_2)
    res = model.fit()
    halflife = np.round(-np.log(2)/res.params[1],0)

    return halflife

# Calculate ZScore
def calculate_zscore(spread):
    spread_series = pd.Series(spread)
    mean = spread_series.rolling(window=WINDOW, center=False).mean()
    std = spread_series.rolling(window=WINDOW, center=False).std()
    x = spread_series.rolling(window=1, center=False).mean()
    zscore = (x - mean)/std
    return zscore

# Calculate Cointegration
def cointegration(series_1, series_2):
    series_1 = np.array(series_1).astype(float)
    series_2 = np.array(series_2).astype(float)
    coint_flag = 0
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0]
    p_value = coint_res[1] # IF <0.05 we have statisticall evidence to say it is cointegrated
    critical_value = coint_res[2][1]

    # How do we know if it is cointegrated?
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]

    # Calculate spread
    spread = series_1 - hedge_ratio *  series_2
    half_life = calculate_halflife(spread)

    # Tcheck: t-value < critical value, FOR THIS LIBRARY
    # Tipically it should be t-value>critical value
    t_check = coint_t < critical_value
    coint_flag = 1 if p_value < 0.05 and t_check else 0
    
    # Return
    return coint_flag, hedge_ratio, half_life

# Store cointegration results
def store_cointegration_results(df_market_prices):
    '''
    Store cointegration results
    '''
    # Initialize
    markets = df_market_prices.columns.to_list()
    criteria_met_pairs = []

    # Find cointegrated pairs
    # Start with base pair
    # print(df_market_prices)

    # We now need to cross validate all pairs against each other to look for cointegration
    for index, base_market in enumerate(markets[:-1]):
        series_1 = df_market_prices[base_market].values.astype(float).tolist() # getting the market, and the price values as floats
        
        # Get Ticker pair
        for quote_market in markets[index+1:]: # we got the market, we need to start from the next index onwards
            series_2 = df_market_prices[quote_market].values.astype(float).tolist()

            # Now we need to make sure they are cointegrated
            # Check cointegration
            coint_flag, hedge_ratio, half_life = cointegration(series_1, series_2)

            # Log pair
            if coint_flag == 1 and half_life <= MAX_HALF_LIFE and half_life >0:
                criteria_met_pairs.append({
                    "base_market": base_market,
                    "quote_market": quote_market,
                    "hedge_ratio": hedge_ratio,
                    "half_life": half_life
                })
    # Create and save DataFrame
    df_criteria_met = pd.DataFrame(criteria_met_pairs)
    df_criteria_met.to_csv('data/cointegrated_pairs.csv')
    pprint(df_criteria_met)
    del df_criteria_met

    # Return results
    print("Cointegrated pairs succesfully saved")
    return "saved"