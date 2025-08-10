"""
Main function to run the snow_load_servie

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

def run_service():
    """
    Main to run the service
    :return:
    """

    # Load snow formula
    with open("snow_formula.json", 'r') as fd:
        formulas = json.load(fd)

    # Load the PORT from the .env
    load_dotenv()
    port = os.getenv("PORT_SNOW")
    token = os.getenv("ASCE_HAZARD_TOOL_TOKEN_SNOW")

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

        url = "https://api-hazard.asce.org/v1/snow"

        req_data = {
            "lat": recv_data["lat"],
            "lon": recv_data["lon"],
            "standardsVersion": recv_data["standardsVersion"],
            "riskLevel": recv_data["riskLevel"]
        }

        api_data = get_request(url, recv_data, token)

        if "Error" not in api_data:
            ground_snow_load = float(api_data.get("snow", {}).get("snowResults",
                        [{}])[0].get("features", [{}])[0].get("attributes",
                                {}).get("Display_1"))

            f_val = {
                'Ce': recv_data['Ce'],
                'Ct': recv_data['Ct'],
                'I': recv_data['I'],
                'Pg': ground_snow_load
            }

            building_code = recv_data["Building Code"]

            r = formula_eval(f_val, formulas[building_code]["pf"]["expression"])

            # Send calculated now load to client
            send_message_json(socket, {
                "Ground Snow Load (psf)": ground_snow_load,
                "Flat Ground Snow Load (psf)": r
            })
        else:
            send_message_json(socket, api_data)


if __name__ == "__main__":
    run_service()
