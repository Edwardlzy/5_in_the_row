class State:
    """A class to store data of each step of a move."""

    def __init__(self, map_size, curr_map, poss_locs, step=0):
        self.map_size = map_size
        self.step = step
        self.curr_map = curr_map # this is a dictionary. keys are tuples, (x,y). values are either 0 or 1.
        self.poss_locs = poss_locs # this is a set store all possible moves. in (x,y) form.

    def new_step(self, vertex, who):
        self.curr_map[vertex] = who
        self.step += 1
        if vertex in self.poss_locs:
            self.poss_locs.discard(vertex)
        x, y = vertex[0], vertex[1]
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                new_possible = (x + i, y + j)
                if new_possible not in self.curr_map and new_possible not in self.poss_locs:
                    if new_possible[0] >= 0 and new_possible[0] < self.map_size and new_possible[1] >= 0 and new_possible[1] < self.map_size:
                        self.poss_locs.add(new_possible)
        for i in range(-3, 4, 3):
            for j in range(-3, 4, 3):
                new_possible = (x + i, y + j)
                if new_possible not in self.curr_map and new_possible not in self.poss_locs:
                    if new_possible[0] >= 0 and new_possible[0] < self.map_size and new_possible[1] >= 0 and \
                                    new_possible[1] < self.map_size:
                        self.poss_locs.add(new_possible)

    def isWin(self, loc, who):
        def one_direction(loc, x, y, who):
            p, q = loc[0], loc[1]
            a, b = - 4 * x, - 4 * y
            i, count = 0, 0
            while i < 9:
                check_loc = (p + a, q + b)
                if check_loc in self.curr_map and self.curr_map[check_loc] == who:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
                i, a, b = i+1, a+x, b+y
            return False

        for i in range(4):
            x, y = [1, 1, 0, -1][i], [1, 0, 1, 1][i]
            if one_direction(loc, x, y, who):
                return 1
        return 0





    def __str__(self):
        return self.curr_map