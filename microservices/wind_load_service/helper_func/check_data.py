"""
Helper function to check data requested from the client

Includes:
- check_data()
"""

def check_data(data:dict):
    """
    Checks the data requested from the client and returns if the data is
    valid or invalid with the invalid response message.
    :param data: arr, Data requested from the client
    :return: bool, str
    """

    req_key = ['lat', 'lon', 'standardsVersion', 'riskLevel', 'MRI', 'z',
               'zg', 'alpha', 'Kzt', 'Ke', 'Kd', 'Building Code']
    message = {}

    if len(data) != len(req_key):
        message["Error"] = "Received Invalid Data!"
        return False, message

    for key, value in data.items():
        if key not in req_key:
            message["Error"] = "Received Invalid Keys!"
            return False, message

    return True, message
