"""
Helper functions for ZeroMQ pipeline communication

Includes:
- setup_socket_server()
- setup_socket_client()
- recv_message_str()
- send_message_str()
- recv_message_json()
- send_message_json()
"""

import zmq

def setup_socket_server(port=5600):
    """
    Sets up ZeroMQ server socket bound to the specified port.
    :param port: int, Port Number
    :return: zmq.socket
    """

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")

    print(f"[weather-packing-service] listening on tcp://*:{port}")
    return socket

def setup_socket_client(port=5600):
    """
    Sets up ZeroMQ client socket bound to the specified port.
    :param port: int, Port Number
    :return: zmq.socket
    """

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")

    return socket

def recv_message_str(socket):
    """
    Receives a string message from the given ZMQ Socket.
    :param socket: zmq.socket
    :return: str, The received message
    """

    message = socket.recv()
    return message

def send_message_str(socket, message):
    """
    Sends a string message from the given ZMQ Socket.
    :param socket: zmq.socket
    :param message: str, String to be sent
    :return: None
    """

    socket.send_string(message)

def recv_message_json(socket):
    """
    Receives a json message from the given ZMQ Socket.
    :param socket: zmq.socket
    :return: list, The received message
    """

    message = socket.recv_json()
    return message

def send_message_json(socket, message):
    """
    Sends a json message from the given ZMQ Socket.
    :param socket: zmq.socket
    :param message: list, JSON to be sent
    :return: None
    """

    socket.send_json(message)