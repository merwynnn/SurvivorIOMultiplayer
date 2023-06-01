import random
import string
import numpy as np

class Player:
    def __init__(self, username, websocket):
        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link
        self.username = username
        self.session = None
        self.websocket = websocket

        self.position = np.array((0, 0))

