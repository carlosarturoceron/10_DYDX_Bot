from func_private import place_market_order, check_order_status

from datetime import datetime, timedelta
import time

from pprint import pprint # pretty print

# Class: Agent for managing and checking trades
class BotAgent:
    """
    Primary function of BotAgent handles opening and checking order status
    """

    # Initialize class
    def __init__(
            self,
            client,
            market_1,
            market_2,
            base_side,
            base_size,
            base_price,
            pair_side,
            pair_size,
            pair_price,
            accept_failsafe_base_price,
            z_score,
            half_life,
            hedge_ratio
        ):

        # Initialize class variables
        self.client = client
        self.market_1 = market_1
        self.market_2 = market_2
        self.base_side = base_side
        self.base_size = base_size
        self.base_price = base_price
        self.pair_side = pair_side
        self.pair_size = pair_size
        self.pair_price = pair_price
        self.accept_failsafe_base_price = accept_failsafe_base_price
        self.z_score = z_score
        self.half_life = half_life
        self.hedge_ratio = hedge_ratio
    
        # Initialize output variable
        # Pair status options are FAILED, LIVE, CLOSE, ERROR
        self.order_dict = {
                "market_1": market_1,
                "market_2": market_2,
                "hedge_ratio": hedge_ratio,
                "z_score": z_score,
                "half_life": half_life,
                "order_id_m1": "",
                "order_m1_side": base_side,
                "order_m1_size": base_size,
                "order_m1_time": "",
                "order_id_m2": "",
                "order_m2_side": pair_side,
                "order_m2_size": pair_size,
                "order_m2_time": "",
                "pair_status": "",
                "comments": ""
        }

    # Check order status by id
    def check_order_status_by_id(self, order_id):
        # Allow time to process
        time.sleep(2)

        # Check order status
        order_status = check_order_status(client=self.client, order_id=order_id)

        # Guard: If order CANCELED move on to next Pair
        if order_status == "CANCELED":
            print(f"{self.market_1} vs {self.market_2} - Order CANCELED 1...")
            self.order_dict['pair_status'] = "FAILED"
            return "FAILED"
        
        # Guard: If order not filled wait util order expiration
        if order_status != "FILLED":
            time.sleep(15)
            order_status = check_order_status(client=self.client, order_id=order_id)
            # Guard: IF order CANCELED move on to next pair
            if order_status == "CANCELED":
                print(f"{self.market_1} vs {self.market_2} - Order CANCELED 2...")
                self.order_dict['pair_status'] = "FAILED"
                return "FAILED"
            
            # Guard: IF not filled, cancel order
            if order_status != "FILLED":
                self.client.private.cancel_order(order_id=order_id)
                self.order_dict["pair_status"] = "ERROR"
                print(f"{self.market_1} vs {self.market_2} - Order ERROR 3...")
                return "ERROR"
        
        # Return check_order_status_by_id
        return "LIVE"

    # Open trades
    def open_trades(self): 
        
        # Print status
        print("---"*10)
        print(f"{self.market_1}: Placing first order....")
        print(f"Side: {self.base_side} | Size: {self.base_size} | Price: {self.base_price}")
        print("---"*10)

        # Place Base Order
        try:
            base_order = place_market_order(
                self.client,
                market=self.market_1,
                side=self.base_side,
                size=self.base_size,
                price=self.base_price,
                reduce_only=False # we are not closing, ONLY want to open
            )
            print("BASE ORDERRRR \n", base_order.data)
            # Store the order id
            self.order_dict["order_id_m1"] = base_order.data["order"]["id"]
            self.order_dict["order_m1_time"] = datetime.now().isoformat()
        except Exception as e:
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"Market 1 {self.market_1}: {e}"
        
        # Make sure order is LIVE before processing
        print("MAKING SURE ORDER IS LIVE 1")
        order_status_m1 = self.check_order_status_by_id(self.order_dict["order_id_m1"])

        # Guard: ABORT if order failed
        print("ORDER STATUS BASE ASSET", order_status_m1)
        if order_status_m1 != "LIVE":
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"FAILED TO FILL {self.market_1}"
            return self.order_dict

        # Print status - Opening SECOND ORDER
        print("---"*10)
        print(f"{self.market_2}: Placing SECOND order....")
        print(f"Side: {self.pair_side} | Size: {self.pair_size} | Price: {self.pair_price}")
        print("---"*10)

        # Place PAIR Order
        try:
            pair_order = place_market_order(
                self.client,
                market=self.market_2,
                side=self.pair_side,
                size=self.pair_size,
                price=self.pair_price,
                reduce_only=False # we are not closing, ONLY want to open
            )

            # Store the order id
            self.order_dict["order_id_m2"] = pair_order.data["order"]["id"]
            self.order_dict["order_m2_time"] = datetime.now().isoformat()
        except Exception as e:
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"Market 2 {self.market_2}: {e}"

        # Make sure order is LIVE before processing
        print("MAKING SURE ORDER 2 IS LIVE BEFORE PROCESSING")
        order_status_m2 = self.check_order_status_by_id(self.order_dict["order_id_m2"])

        # Guard: ABORT if order failed
        print("ORDER 2 STATUS", order_status_m2)
        if order_status_m2 != "LIVE":
            print("ORDER 2 STATUS FAILED", order_status_m2, "CLOSING ORDER 1")
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"FAILED TO FILL {self.market_2}"
        
            # IF Order 1 PASSED, BUT ORDER 2 FAILED. WE NEED TO CLOSE ORDER 1!!
            # Closing order 1
            try:
                close_order = place_market_order(
                    self.client,
                    market=self.market_1,
                    side=self.pair_side, # we use the SIDE of PAIR, because we the order is open and we need to close it
                    size=self.base_size,
                    price=self.accept_failsafe_base_price, # price precalculated so we know exit price, in case we need to close it
                    reduce_only=True # True: Because we are CLOSING
                )
                print('WE PLACED ORDER TO CLOSE ORDER 1 BC ORDER 2 FAILED')
                # Make sure order is LIVE before proceeding
                time.sleep(2)
                print("CHECKING CLOSING ORDER 1 STATUS")
                order_status_close_order = check_order_status(self.client, close_order.data["order"]["id"])
                print("WE CHECKED STATUS", order_status_close_order)
                # Here is where you need communication
                # SEND MESSAGE TO OPERATOR
                # HEY SOMETHING FAILED, YOU ARE NOW OPEN, W/O ARBITRAGE
                if order_status_close_order != "FILLED":
                    print("ABORT PROGRAM")
                    print("+++++UNEXPECTED ERROR++++")
                    print(order_status_close_order)
                    
                    # !!! CONSIDER SENDING ORDER MESSAGE HERE !!!

                    # ABORT
                    exit(1)

            except Exception as e:
                self.order_dict["pair_status"] = "ERROR"
                self.order_dict["comments"] = f"ERROR CLOSING m_1 {self.market_1}: {e}"
                print("ABORT PROGRAM")
                print("+++++UNEXPECTED ERROR++++")
                print(order_status_close_order)

                # !!! CONSIDER SENDING ORDER MESSAGE HERE !!!

                # ABORT
                exit(1)
        
        else:
            self.order_dict["pair_status"] = "LIVE"
            return self.order_dict
