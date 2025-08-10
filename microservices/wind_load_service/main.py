"""
Main function to run the wind_load_servie

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

    # Load wind formula
    with open("wind_formula.json", 'r') as fd:
        formulas = json.load(fd)

    # Load the PORT from the .env
    load_dotenv()
    port = os.getenv("PORT_WIND")
    token = os.getenv("ASCE_HAZARD_TOOL_TOKEN_WIND")

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

        url = "https://api-hazard.asce.org/v1/wind"

        req_data = {
            "lat": recv_data["lat"],
            "lon": recv_data["lon"],
            "standardsVersion": recv_data["standardsVersion"],
            "riskLevel": recv_data["riskLevel"]
        }

        api_data = get_request(url, req_data, token)

        if "Error" not in api_data:
            f_val = {
                'z': recv_data['z'],
                'zg': recv_data['zg'],
                'alpha': recv_data['alpha'],
                'Kzt': recv_data['Kzt'],
                'Ke': recv_data['Ke'],
                'Kd': recv_data['Kd'],
                'V': float(api_data["wind"]["mriWindResults"][recv_data['MRI']])
            }

            building_code = recv_data["Building Code"]
            if formula_eval(f_val, formulas[building_code]["Kz"]["condition"]):
                r = formula_eval(f_val, formulas[building_code]["Kz"][
                    "true_expression"])
            else:
                r = formula_eval(f_val, formulas[building_code]["Kz"][
                    "false_expression"])

            f_val["Kz"] = r

            r = formula_eval(f_val, formulas[building_code]["qz"]["expression"])

            # Send calculated load to client
            send_message_json(socket, {
                "Wind Speed (mph)": f_val['V'],
                "qz (psf)": r
            })
        else:
            send_message_json(socket, api_data)

if __name__ == "__main__":
    run_service()
