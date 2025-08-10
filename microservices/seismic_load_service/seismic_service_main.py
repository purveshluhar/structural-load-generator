"""
Main function to run the seismic_load_servie

Includes:
- run_service()
"""

from dotenv import load_dotenv
import os
from helper_func.request import get_request
from helper_func.socket_handler import (setup_socket_server,
                                        send_message_json, recv_message_json)
from helper_func.check_data import check_data
from helper_func.simple_eval import formula_eval
import json
import sys


def run_service():
    """
    Main to run the service
    :return:
    """

    # Load seismic formula
    with open("seismic_formula.json", 'r') as fd:
        formulas = json.load(fd)

    # Load the PORT from the .env
    load_dotenv()
    port = os.getenv("PORT_SEISMIC")

    # Set up the socket
    socket = setup_socket_server(port)

    while True:
        # Request data from client
        recv_data = recv_message_json(socket)

        is_valid, message = check_data(recv_data)

        # If not valid data type
        if not is_valid:
            send_message_json(socket, message)
            continue

        url = "https://earthquake.usgs.gov/ws/designmaps/asce7-16.json"
        req_data = {
            "latitude": recv_data["latitude"],
            "longitude": recv_data["longitude"],
            "riskCategory": recv_data["riskCategory"],
            "siteClass": recv_data["siteClass"],
            "title": recv_data["title"]
        }

        api_data = get_request(url, req_data)

        if "Error" not in api_data:
            f_val = {
                "Sds": api_data["response"]["data"]["sds"],
                "R": recv_data["R"],
                "I": recv_data["I"]
            }

            # Calculate Cs
            r = formula_eval(f_val, formulas[recv_data["Building Code"]][
                "Cs"]["expression"])

            # Calculate V
            f_val = {
                "Cs": r,
                "W": recv_data["W"]
            }

            # Calculate V
            r = formula_eval(f_val, formulas[recv_data["Building Code"]][
                "V"]["expression"])

            # Send calculated load to client
            send_message_json(socket, {
                "Base Shear (V)": r,
                "Ss": api_data["response"]["data"]["ss"],
                "S1": api_data["response"]["data"]["s1"],
                "Sds": api_data["response"]["data"]["sds"],
                "Sd1": api_data["response"]["data"]["sd1"],
                "Seismic Response Coefficient, Cs": f_val["Cs"]
            })

        else:
            send_message_json(socket, api_data)


if __name__ == "__main__":
    run_service()
