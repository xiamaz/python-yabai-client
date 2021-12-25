import json
import socket
import pathlib


BUFFER_SIZE = 8096


class YabaiClient:
    """Client for yabai UNIX socket calls."""

    def __init__(self):
        yabai_sockets = list(pathlib.Path("/tmp").glob("yabai_*.socket"))
        self._yabai_socket = str(yabai_sockets[0])

    def send_message(self, message):
        cleaned_message = message.replace(" ", "\0") + "\0"
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(self._yabai_socket)
            sock.sendall(str.encode(cleaned_message))
            sock.shutdown(socket.SHUT_WR)
            recv = str(sock.recv(BUFFER_SIZE), "utf-8")

        data = json.loads(recv)
        return data
