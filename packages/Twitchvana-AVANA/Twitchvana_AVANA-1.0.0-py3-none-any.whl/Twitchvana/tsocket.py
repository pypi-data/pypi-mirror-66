from socket import socket
from .irc_settings import HOST, PORT

class TSocket(socket):
    """
        Twitch socket.
    """
    def __init__(self, PASS : str, USER : str):
        super().__init__()
        self.connect((HOST, PORT))

        self.send(f'PASS {PASS}')
        self.send(f'NICK {USER.lower()}')

    def send(self, msg):
        """
            Wrapper for send, takes a literal string and turns it into a byte-like objects and appends the "\\r\\n" tag at the end.
        """
        super().send(f'{msg}\r\n'.encode())

def create_socket(PASS: str, USER: str):
    """
        Creates a TSocket and logs into the twitch irc server.

        Returns : TSocket
    """
    return TSocket(PASS, USER)