import json
import socket
import select
import pathlib


BUFFER_SIZE = 8096


class YabaiClient:
    """Client for yabai UNIX socket calls."""

    def __init__(self):
        yabai_sockets = list(pathlib.Path("/tmp").glob("yabai_*.socket"))
        self._yabai_socket = str(yabai_sockets[0])

    def send_message(self, *message, expect_result=True):
        tries = 5
        for _ in range(tries):
            try:
                result = self._send_message(*message, expect_result=expect_result)
                break
            except json.JSONDecodeError as err:
                continue
        else:
            raise RuntimeError(f"Failed to send message after {tries} attempts.")
        return result

    def _send_message(self, *message, expect_result=True):
        cleaned_message = "\0".join(message) + "\0\0"


        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(self._yabai_socket)
            sent = sock.send(str.encode(cleaned_message))
            sock.shutdown(socket.SHUT_WR)

            poller = select.poll()
            poller.register(sock, select.POLLIN)
            msg = ""
            while True:
                poller.poll()
                recv = str(sock.recv(BUFFER_SIZE), "utf-8")

                msg += recv

                if len(recv) == 0:
                    break

            if expect_result:
                data = json.loads(msg)
            else:
                data = None

        return data
