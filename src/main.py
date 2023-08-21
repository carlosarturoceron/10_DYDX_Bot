from connections import connect_dydx
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES
from func_private import abort_all_positions
from utils.func_public import construct_market_prices
from utils.cointegration import store_cointegration_results
from bot.entry_pairs import open_positions

if __name__ == '__main__':

    # Connect to client
    try:
        print('Connecting to client...')
        client = connect_dydx()
        print(client.private.get_account().data)

    except Exception as e:
        print('Error connecting to client:', e)
        exit(1)

    # Abort all open positions (Kill Switch)
    if ABORT_ALL_POSITIONS == True:
        try:
            print('Closing all positions...')
            kill_switch = abort_all_positions(client)
            print('This are the positions that where closed by the kill switch:', kill_switch)
        except Exception as e:
            print('Error in Kill Switch', e)

    # Finding cointegrated pairs
    if FIND_COINTEGRATED == True:
        
        # Construct Market Prices
        try:
            print('Fetching market prices, pelase allow 3 mins...')
            df_market_prices = construct_market_prices(client=client)
        except Exception as e:
            print('Error constructing market prices all positions...', e)
            exit(1)

        # Store Cointegrated Pairs
        try:
            print('Storing Cointegrated pairs...')
            stores_resulst = store_cointegration_results(df_market_prices)
            if stores_resulst != "saved":
                print('...')
                exit(1)
        except Exception as e:
            print('++++++++Exception saving cointegrated pairs...', e)
            exit(1)

    #  ---------ROOM FOR OTHER CODE---------
    # Managing Existing Trades, While loop

        # Place trades for opening positions
    # Finding cointegrated pairs
    if PLACE_TRADES == True:
        
        # Construct Market Prices
        try:
            print('Finding trading opportunities...')
            open_positions(client)
        except Exception as e:
            print('Error PLACING TRADES...', e)
            exit(1)