from connections import connect_dydx
from constants import ABORT_ALL_POSITIONS
from func_private import abort_all_positions

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

