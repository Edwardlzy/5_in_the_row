
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

    def __eq__(self, other):
        for i in self.curr_map:
            if i not in other.curr_map:
                return False
            if self.curr_map[i] != other.curr_map[i]:
                return False
        return True

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
        # for i in range(-3, 4, 3):
        #     for j in range(-3, 4, 3):
        #         new_possible = (x + i, y + j)
        #         if new_possible not in self.curr_map and new_possible not in self.poss_locs:
        #             if new_possible[0] >= 0 and new_possible[0] < self.map_size and new_possible[1] >= 0 and \
        #                             new_possible[1] < self.map_size:
        #                 self.poss_locs.add(new_possible)

    def isWin(self, loc, who):
        def one_direction(loc, x, y, who):
            tempS = ""
            for i in range(-5, 6):
                m, n = loc[0] + x * i, loc[1] + y * i
                if m >= 0 and n >= 0 and m < self.map_size and n < self.map_size:
                    new_loc = (m, n)
                    if new_loc not in self.curr_map:
                        tempS += "-"
                    else:
                        tempS += str(self.curr_map[new_loc])
                else:
                    tempS += "x"
            if "00000" in tempS:
                return float("inf")
            if "11111" in tempS:
                return float("-inf")

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
        # print("loc", loc, ",tempS ", tempS)
        if "00000" in tempS:
            return float("inf")
        if "011110" in tempS or tempS.find("11101") == 2 or tempS.find("11101") == 3:
            return 999999
        t = tempS.find("-0000-")
        if t > 0 and t < 5:
            return 29999
        r = 0
        if tempS.find("-1110") == 1:
            r += 3999
        if tempS.find("-11-10") == 0 or tempS.find("-1-110") == 0 or tempS.find("-1101-") == 2:
            r += 3900
        t = tempS.find("0-0001")
        if "-00001" in tempS:
            r += 250
        if "0-0001" in tempS or "00-001" in tempS or "000-01" in tempS:
            r += 220
        t = tempS.find("-000-")
        if t > 1 and t < 5:
            r += 100
        t = tempS.find("-00-0-")
        if t > 0 and t < 5:
            r += 120
        if tempS.find("-01110") == 0:
            r += 55
        if tempS.find("-110") == 2:
            r += 50
        if tempS.find("-101-") == 3:
            r += 25
        if tempS.find("-00-") == 3:
            r += 25
        if tempS.find("-1-01-") == 2:
            r += 30
        if tempS.find("-0-0-") == 2 or tempS.find("-0--0-") == 1:
            r += 20
        if tempS.find("-10-") == 3:
            r += 8
        return r

    def check_all_directions(self, loc, state):
        e = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0:
                    a = self.check_each(loc, x, y, state)
                    # print("(x, y) is", (x, y), "eva result,", a)
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
            # print("loc is", loc, "eva result,", t)
            if t >= 999999:
                return loc
            if m < t:
                m = t
                l = [loc]
            elif m == t:
                l.append(loc)
        return choice(l)

    def minimaxFn(self, depth):
        def mmfn(s, loc, who, depth):
            if s.isWin(loc, who):
                return float("inf") if who == 0 else float("-inf")
            if depth == 0:
                u = self.check_all_directions(loc, s)
                print("at bottom u is", u, ", loc is", loc)
                return u
            w = 1 - who
            c = float("-inf") if w == 0 else float("inf")
            for move in s.poss_locs:
                sc = s.copy()
                sc.new_step(move, w)
                if w == 0:
                    t = mmfn(sc, move, w, depth - 1)
                    c = max(c, t)
                else:
                    t = mmfn(sc, move, w, depth - 1)
                    c = min(c, t)
                    print("================")
                print("current move is", move, "depth is", depth, ", who is", w, "(0 means max, 1 means min) , c is", c, ", t is", t)
            # if who == 1:
            #     print("c", c)
            #     exit()
            return c

        y = float("-inf")
        l = []
        for m in self.poss_locs:
            s_copy = self.copy()
            s_copy.new_step(m, 0)
            eva = mmfn(s_copy, m, 0, depth - 1)
            # print("move,", m, ". eva,", eva)
            if y < eva:
                y = eva
                l = [m]
            elif y == eva:
                l.append(m)
        return choice(l)

class dpstorage:
    def __init__(self):
        self.all = dict()

    def hashing(self, s):
        h = 0
        for i in s.curr_map:
            h += i[0] + i[1] + s.curr_map[i]
        return h

    def find(self, s, depth):
        h = self.hashing(s)
        if h in self.all:
            v = self.all[h]
            for i in v:
                if i[0] == s.curr_map and i[1] >= depth:
                    return i[2]
        return False

    def add(self, s, depth, eva):
        h = self.hashing(s)
        if h not in self.all:
            self.all[h] = []
        self.all[h].append([s.curr_map, depth, eva])

# if __name__ == "__main__":
#     pass