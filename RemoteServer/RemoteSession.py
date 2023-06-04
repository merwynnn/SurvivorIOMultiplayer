import string
import random


class RemoteSession:
    def __init__(self, host_websocket):
        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_uppercase + numbers, 4))  # Generate a random link

        self.host = host_websocket

        self.clients_id = {}
        self.websockets = {}