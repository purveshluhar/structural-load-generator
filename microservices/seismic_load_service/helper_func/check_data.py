"""
Helper function to check data requested from the client

Includes:
- check_data()
"""

def check_data(data:bytearray):
    """
    Checks the data requested from the client and returns if the data is
    valid or invalid with the invalid response message.
    :param data: arr, Data requested from the client
    :return: bool, str
    """

    req_key = ['latitude', 'longitude', 'riskCategory', 'siteClass',
               'title', 'R', 'I', 'W', 'Building Code']
    message = {}

    for value in data:
        value:dict
        # Check the received data
        if len(value) != len(req_key):
            message["Error"] = "Received Invalid Data!"
            return False, message
        else:
            for key, cvalue in value.items():
                if key not in req_key:
                    message["Error"] = "Received Invalid Keys, Try again!"
                    return False, message

    return True, message
