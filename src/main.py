from connections import connect_dydx

if __name__ == '__main__':

    # Connect to client
    try:
        client = connect_dydx()
        print(client.private.get_account().data)

    except Exception as e:
        print('Error connecting to client:', e)
        exit(1)