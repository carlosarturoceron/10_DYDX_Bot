from datetime import datetime, timedelta
# Format number
def format_number(current_number, match_num):

    """
    Given a current number as an example for decimals desired
    Function will return the correctly formatted string
    """

    current_number_string = f"{current_number}"
    match_num_string = f"{match_num}"

    if "." in match_num_string:
        match_decimals =  len(match_num_string.split('.')[1])

        current_number_string = f"{current_number:.{match_decimals}f}"
        current_number_string = current_number_string[:]
        return current_number_string
    else:
        return f"{int(current_number)}"

# Aux function for get_ISO_times
def format_time(timestamp):
    return timestamp.replace(microsecond=0).isoformat()

# Get ISO Times

def get_ISO_times():
    
    # Get Timestamps
    date_start_0 = datetime.now() # Get current time
    date_start_1 = date_start_0 - timedelta(hours=100) # What would have been the time 100 hours before now (date_start_0)?
    date_start_2 = date_start_1 - timedelta(hours=100)
    date_start_3 = date_start_2 - timedelta(hours=100)
    date_start_4 = date_start_3 - timedelta(hours=100)
    # The reason we want to do this is because dydx needs 
    # The reason we want to do this is because dydx needs 
    # The reason we want to do this is because dydx needs 
    # The reason we want to do this is because dydx needs 
    # The reason we want to do this is because dydx needs 
    # The reason we want to do this is because dydx needs 
    # fromISO: Starting point for the candles
    # toISO: Ending point for the candles
    
    # Format datetimes
    times_dict = {
        "range_1":{
            "from_iso": format_time(date_start_1),
            "to_iso": format_time(date_start_0)
        },
        "range_2":{
            "from_iso": format_time(date_start_2),
            "to_iso": format_time(date_start_1)
        },
        "range_3":{
            "from_iso": format_time(date_start_3),
            "to_iso": format_time(date_start_2)
        },
        "range_4":{
            "from_iso": format_time(date_start_4),
            "to_iso": format_time(date_start_3)
        }
    }

    # Return result (aprox 16 days of data)
    return times_dict