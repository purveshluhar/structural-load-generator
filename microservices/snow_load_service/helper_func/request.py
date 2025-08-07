"""
Main function to run the seismic_load_servie

Includes:
- get_request()
"""

import requests

def get_request(url, payload:dict, token=None):
    """
    Performs get HTTP request and outputs the response and status code
    :param url:
    :param payload:
    :param token:
    :return:
    """

    if token is not None:
        # Make a copy of the dict
        payload = payload.copy()
        payload["token"] = token

    r = requests.get(url, params=payload)

    # Check if request raises an error
    if r.raise_for_status() is not None:
        return {"Error": r.raise_for_status()}

    return r.json()