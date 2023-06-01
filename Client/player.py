
import numpy as np

class Player:
    def __init__(self, username):
        self.id = None
        self.username = username

        self.position = np.array((0, 0))

