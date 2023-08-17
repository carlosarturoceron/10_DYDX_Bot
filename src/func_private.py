import time
from datetime import datetime, timedelta

from pprint import pprint


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

            print(market, side)
