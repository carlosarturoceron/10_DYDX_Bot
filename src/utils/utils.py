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