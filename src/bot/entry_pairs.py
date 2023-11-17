from constants import ZSCORE_THRESH, USD_PER_TRADE, USD_MIN_COLLATERAL
from utils.func_public import get_candle_recent
from utils.utils import format_number
from utils.cointegration import calculate_zscore
from func_private import is_open_position # check if we have any open position for a given market
from bot.bot_agent import BotAgent # Import BotAgent Class

# Data Wrangling
import pandas as pd
import numpy as np

# Pretty Print
from pprint import pprint

# JSON
import json

def open_positions(client):
    """
    Manages finding triggers for trade entry
    Store trades for managing later with
    EXIT FUNCTION
    """

    # Load cointegrated frames
    df = pd.read_csv("../src/data/cointegrated_pairs.csv", index_col=0)

    # Get markets for reference of: min order size, tick size, etc..
    markets = client.public.get_markets().data

    # Initialize container for BotAgent results
    bot_agents = []

    # Hunting for promising z score triggers
    for index, row in df.iterrows():

        # Extract variables
        base_market = row["base_market"]
        pair_market = row["quote_market"]
        hedge_ratio = row["hedge_ratio"]
        half_life = row["half_life"]

        # Get current prices
        series_1 = get_candle_recent(client=client, market=base_market)
        series_2 = get_candle_recent(client=client, market=pair_market)
    
        # Get z score
        if len(series_1) > 0 and len(series_1) == len(series_2): # sizes need to match
            spread = series_1 - (hedge_ratio * series_2)
            z_score = calculate_zscore(spread=spread).values.tolist()[-1] # get zscores and pass to list

            # Establish if potential trade
            if abs(z_score) >= ZSCORE_THRESH:

                # Make sure like-for-like not already open (diversifying trades)
                is_base_open = is_open_position(client=client, market=base_market)
                is_pair_open = is_open_position(client=client, market=pair_market)

                # Place trade
                if not is_base_open and not is_pair_open:

                    # Determine side
                    base_side = "BUY" if z_score < 0 else "SELL"
                    pair_side = "BUY" if z_score > 0 else "SELL"

                    # Get acceptable price in string format with correct number of decimals
                    base_price = series_1[-1]
                    pair_price = series_2[-1]

                    accept_base_price = float(base_price) * 1.01 if z_score < 0 else float(base_price) * 0.99
                    accept_pair_price = float(pair_price) * 1.01 if z_score > 0 else float(pair_price) * 0.99
                    failsafe_base_price = float(base_price) * 0.05 if z_score < 0 else float(base_price) * 0.99
                    accept_pair_price = float(pair_price) * 1.01 if z_score > 0 else float(pair_price) * 1.7 # this ensures we can close
                    base_tick_size = markets["markets"][base_market]["tickSize"]
                    pair_tick_size = markets["markets"][pair_market]["tickSize"]

                    # Format prices
                    accept_base_price = format_number(accept_base_price, base_tick_size)
                    accept_pair_price = format_number(accept_pair_price, pair_tick_size)
                    accept_failsafe_base_price = format_number(failsafe_base_price, base_tick_size)

                    # Get Size
                    base_quantity = 1 / base_price * USD_PER_TRADE
                    pair_quantity = 1 / pair_price * USD_PER_TRADE
                    base_step_size = markets["markets"][base_market]["stepSize"]
                    pair_step_size = markets["markets"][pair_market]["stepSize"]

                    # Format sizes
                    base_size = format_number(base_quantity, base_step_size)
                    pair_size = format_number(pair_quantity, pair_step_size)

                    # Ensure size
                    base_min_order_size = markets["markets"][base_market]["minOrderSize"]
                    pair_min_order_size = markets["markets"][pair_market]["minOrderSize"]
                    check_base = float(base_quantity) > float(base_min_order_size)
                    check_pair = float(pair_quantity) > float(pair_min_order_size)

                    print("CHECKSSSS", check_base, check_pair)

                    if check_base and check_pair:

                        # Check account balance and get free collateral
                        account = client.private.get_account()
                        free_collateral = float(account.data["account"]["freeCollateral"])
                        print({f"Balance {free_collateral} and minimum at {USD_MIN_COLLATERAL}"})

                        if free_collateral < USD_MIN_COLLATERAL:
                            print("free collateral less than MINIMUM COLLATERAL")
                            break

                        # Create bot agent
                        bot_agent = BotAgent(
                            client,
                            market_1=base_market,
                            market_2=pair_market,
                            base_side=base_side,
                            base_size=base_size,
                            base_price=accept_base_price,
                            pair_side=pair_side,
                            pair_size=pair_size,
                            pair_price=accept_pair_price,
                            accept_failsafe_base_price=accept_failsafe_base_price,
                            z_score=z_score,
                            half_life=half_life,
                            hedge_ratio=hedge_ratio)
                        
                        # Open Trades
                        try:
                            bot_open_dict = bot_agent.open_trades()

                            # Handle success in opening trades
                            if bot_open_dict["pair_status"] == "LIVE":

                                # Appent to list of bot agents
                                bot_agents.append(bot_open_dict)
                                del bot_open_dict

                                # Confirm live status in print
                                print("Trade status: LIVE")
                                print("~~~~~~~")
                        except Exception as e:
                            print("THIS FAILED", index, "BECAUSE", e, "MOVING ON")
                            pass

    # Save Agents
    print({f"Success: {len(bot_agents)} NEW PAIRS LIVE"})
    if len(bot_agents) > 0:
        with open("bot_agents.json", "w") as f:
            json.dump(bot_agents, f)