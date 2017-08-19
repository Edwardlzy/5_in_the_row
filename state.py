class state:
    """A class to store data of each step of a move."""

    def __init__(self, curr_map):
        self.curr_map = curr_map

    def __str__(self):
        return self.curr_map