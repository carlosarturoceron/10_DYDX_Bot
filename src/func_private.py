import time
from datetime import datetime, timedelta

from pprint import pprint

from utils.utils import format_number

# Get existing open positions
def is_open_position(client,market):
    """
    Check if there are open positions for a given market
    """
    # Protect API
    time.sleep(0.2)

    # Get Positions
    all_positions = client.private.get_positions(
        market=market,
        status="OPEN"
    )

    # Determine if open
    if len(all_positions.data["positions"]) >0:
        return True
    else:
        return False

# Check order status
def check_order_status(client,order_id):
    order = client.private.get_order_by_id(order_id)
    if order.data:
        print("ORDER DATA",order.data)
        if "order" in order.data.keys():
            return order.data["order"]["status"]
    return "FAILED CHECKING ORDER STATUS, THERE ARE NO STATUS"

# Place market order
def place_market_order(client,market,side,size,price,reduce_only):

    # Get position ID
    account_response = client.private.get_account()
    position_id = account_response.data['account']['positionId']
    print(position_id)

    # Get expiration time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(server_time.data['iso'].replace('Z','')) + timedelta(seconds=70)
    expiration

    # Order Variables
    order_type = 'MARKET'
    post_only = False
    limit_fee = '0.015'
    expiration_epoch_seconds = expiration.timestamp()
    time_in_force = 'FOK'
    reduce_only = False

    # Placing the orders
    placed_order = client.private.create_order(
      position_id=position_id, # required for creating the order signature
      market=market,
      side=side,
      order_type=order_type,
      post_only=post_only,
      size=size,
      price=price,
      limit_fee=limit_fee,
      expiration_epoch_seconds=expiration_epoch_seconds,
      time_in_force=time_in_force,
      reduce_only= reduce_only
    )

    print('order placed successfully')
    return placed_order

# Abort all open positions
def abort_all_positions(client):

    # Cancel open orders
    client.private.cancel_all_orders()

    # Protect API
    time.sleep(0.5)

    # Get markets for reference of ticksize
    markets = client.public.get_markets().data
    time.sleep(0.25)
    pprint(markets)

    # Get all open positions
    positions = client.private.get_positions(status='OPEN')
    all_position = positions.data['positions']

    # Handle open positions
    closed_orders = []

    if len(all_position) > 0:
        
        # Loop trough each position
        for position in all_position:
            
            # Get market
            market = position['market']

            # Determine Side
            side = 'BUY'
            if position['side'] == 'LONG':
                side = 'SELL'

            # Getting the price
            price = float(position['entryPrice'])
            accept_price = price * 1.7 if side == 'BUY' else price * 0.3 # Multiplier for worst acceptable price
            tick_size = markets['markets'][market]['tickSize']
            accept_price = format_number(accept_price, tick_size) # Function that formats the price to dydx acceptable's decimals


            print('Placing order...')
            # Place order to close
            order = place_market_order(
                client=client,
                market=market,
                side=side,
                size=position['sumOpen'],
                price= accept_price,
                reduce_only=True # True because it is an open position that we want to close
            )       
            print(order.data)
            # Append the result
            closed_orders.append(order.data)

            # Protect API
            time.sleep(0.2)

        # Returned closed orders
        return closed_orders