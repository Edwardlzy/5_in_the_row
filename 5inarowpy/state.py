class State:
    """A class to store data of each step of a move."""

    def __init__(self, map_size, curr_map, poss_moves):
        self.map_size = map_size
        self.curr_map = curr_map # this is a dictionary. its indexs are tuples, (x,y), and its values can either be 0 or 1.
        self.poss_moves = poss_moves # this is a set store all possible moves. in (x,y) form.

    def new_step(self, vertex, who):
        self.curr_map[vertex] = who
        if vertex in self.poss_moves:
            self.poss_moves.discard(vertex)
        x, y = vertex[0], vertex[1]
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                new_possible = (x + i, y + j)
                if new_possible not in self.curr_map and new_possible not in self.poss_moves:
                    if new_possible[0] >= 0 and new_possible[0] < self.map_size and new_possible[1] >= 0 and new_possible[1] < self.map_size:
                        self.poss_moves.add(new_possible)

    def is_win(self):
        pass

    def is_loss(self):
        pass

    def __str__(self):
        return self.curr_map