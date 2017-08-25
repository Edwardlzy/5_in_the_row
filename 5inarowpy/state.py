
from random import choice

computer = 0
human = 1

class State:
    """A class to store data of each step of a move."""

    def __init__(self, map_size, curr_map, poss_locs):
        self.map_size = map_size
        # self.step = step
        self.curr_map = curr_map # this is a dictionary. keys are tuples, (x,y). values are either 0 or 1.
        self.poss_locs = poss_locs # this is a set store all possible moves. in (x,y) form.

    def copy(self):
        return State(self.map_size, self.curr_map.copy(), self.poss_locs.copy())

    def new_step(self, vertex, who):
        self.curr_map[vertex] = who
        # self.step += 1
        if vertex in self.poss_locs:
            self.poss_locs.discard(vertex)
        x, y = vertex[0], vertex[1]
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                new_possible = (x + i, y + j)
                # Add new valid possible moves to self.poss_locs
                if new_possible not in self.curr_map and new_possible not in self.poss_locs:
                    if new_possible[0] >= 0 and new_possible[0] < self.map_size and new_possible[1] >= 0 and \
                                    new_possible[1] < self.map_size:
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
                return True
        return False

    def check_each(self, loc, x, y, state):
        tempS = ""
        for i in range(-5, 6):
            m, n = loc[0] + x * i, loc[1] + y * i
            if m >= 0 and n >= 0 and m < self.map_size and n < self.map_size:
                new_loc = (m, n)
                if new_loc not in state.curr_map:
                    tempS += "-"
                else:
                    tempS += str(state.curr_map[new_loc])
            else:
                tempS += "x"
        print("loc", loc, ",tempS ", tempS)
        if "00000" in tempS:
            return 999999
        if "011110" in tempS or "11101" in tempS or "11011" in tempS:
            return 99999
        t = tempS.find("-0000-")
        if t > 0 and t < 5:
            return 49999
        if tempS.find("-1110") == 1:
            return 999
        if tempS.find("-11-10") == 0 or tempS.find("-1-110") == 0 or tempS.find("-1101-") == 2:
            return 990
        t = tempS.find("-000-")
        if t > 1 and t < 5:
            return 10
        t = tempS.find("-00-0-")
        if t > 0 and t < 5:
            return 12
        if tempS.find("-110") == 2:
            return 5
        if tempS.find("-101-") == 3:
            return 2
        if tempS.find("-00-") == 3:
            return 4
        if tempS.find("-1-01-") == 2:
            return 3
        if tempS.find("-0-0-") == 2 or tempS.find("-0--0-") == 1:
            return 2
        if tempS.find("-10-") == 3:
            return 1
        return 0

    def check_all_directions(self, loc, state):
        e = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0:
                    a = self.check_each(loc, x, y, state)
                    if a > 40000:
                        return a
                    e += a
        return e

    def eva_fn(self):
        m = -1
        l = []
        for loc in self.poss_locs:
            state_copy = self.copy()
            state_copy.new_step(loc, 0)
            t = self.check_all_directions(loc, state_copy)
            if t >= 999999:
                return loc
            if m < t:
                m = t
                l = [loc]
            elif m == t:
                l.append(loc)
        return choice(l)

    def mnimaxFn(self, depth):
        def mmfn(s, loc, who, depth):
            s_copy = s.copy()
            s_copy.new_step(loc, who)
            d = depth - 1
            if s_copy.isWin(loc, who):
                if who == 0:
                    return 999999
                else:
                    return -999999
            if d == 0:
                return s_copy.check_all_directions(loc, s_copy)
            c = 0
            for move in s_copy.poss_locs:
                if who == 0: # computer
                    c = max(c, mmfn(s_copy, move, 1, d))
                else: #human
                    c = min(c, mmfn(s_copy, move, 1, d))
            return c

        c = 0
        l = []
        for m in self.poss_locs:
            eva = mmfn(self, m, 0, depth)
            # print("move,", m, ". eva,", eva)
            if c < eva:
                c = eva
                l = [m]
            elif c == eva:
                l.append(m)
        return choice(l)

    def __str__(self):
        return self.curr_map