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

def run_service():
    """
    Main to run the service
    :return:
    """

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

        data = get_request(url, recv_data, token)


if __name__ == "__main__":
    run_service()
