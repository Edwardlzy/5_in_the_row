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
        return State(self.map_size, self.curr_map, self.poss_locs)

    def new_step(self, vertex, who):
        self.curr_map[vertex] = who
        # self.step += 1
        if vertex in self.poss_locs:
            self.poss_locs.discard(vertex)
        x, y = vertex[0], vertex[1]
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                new_possible = (x + i, y + j)
                print("new possible")
                print(new_possible)
                # Add new valid possible moves to self.poss_locs
                if new_possible not in self.curr_map and new_possible not in self.poss_locs:
                    if new_possible[0] >= 0 and new_possible[0] < self.map_size and new_possible[1] >= 0 and \
                                    new_possible[1] < self.map_size:
                        print("new possible")
                        print(new_possible)
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

    def eva_fn(self):
        def check_all_directions(loc):
            e = -1
            for i in range(4):
                x, y = [1, 1, 0, -1][i], [1, 0, 1, 1][i]
                e = max(e, check_each(loc, x, y))
            return e

        def generateloc(loc, x, y, i):
            p, q = loc[0], loc[1]
            return (p + i * x, q + i * y)

        def check_each(loc, x, y):
            r = 0
            new_loc = generateloc(loc, x, y, 1)
            if new_loc not in self.curr_map: # O_
                return 0
            elif self.curr_map[new_loc] == human: # Ox
                new_loc = generateloc(loc, x, y, 2)
                if new_loc in self.curr_map and self.curr_map[new_loc] == human:  # Oxx
                    new_loc = generateloc(loc, x, y, 3)
                    if new_loc in self.curr_map and self.curr_map[new_loc] == human: # Oxxx
                        if generateloc(loc, x, y, 4) in self.curr_map and \
                                        self.curr_map[generateloc(loc, x, y, 4)] == human:  # Oxxxx
                            return 99999
                        elif generateloc(loc, x, y, -1) in self.curr_map and \
                                        self.curr_map[generateloc(loc, x, y, -1)] == human:  # xOxxx
                            return 99999
                        elif generateloc(loc, x, y, 4) not in self.curr_map and \
                                        generateloc(loc, x, y, 5) not in self.curr_map: # Oxxx__
                            r += 999
                new_loc = generateloc(loc, x, y, -1)
                if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # oOx
                    new_loc = generateloc(loc, x, y, -2)
                    if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # ooOx
                        new_loc = generateloc(loc, x, y, -3)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # oooOx
                            if generateloc(loc, x, y, -4) not in self.curr_map: # _oooOx
                                return r + 17
                        elif new_loc not in self.curr_map and \
                            generateloc(loc, x, y, -4) not in self.curr_map: # __ooOx
                            return r + 2
                return r
            else: # Oo
                new_loc = generateloc(loc, x, y, 2)
                if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # Ooo
                    new_loc = generateloc(loc, x, y, 3)
                    if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # Oooo
                        if (generateloc(loc, x, y, 4) in self.curr_map and
                                        self.curr_map[generateloc(loc, x, y, 4)] == computer) or \
                            (generateloc(loc, x, y, -1) in self.curr_map and
                                        self.curr_map[generateloc(loc, x, y, -1)] == computer):
                            return 999999
                        if generateloc(loc, x, y, 4) not in self.curr_map and \
                                        generateloc(loc, x, y, -1) not in self.curr_map: # _Oooo_
                            return 49999
                        if generateloc(loc, x, y, 4) in self.curr_map and \
                                        generateloc(loc, x, y, -1) not in self.curr_map: # _Oooox
                            return 17
                        if generateloc(loc, x, y, 4) not in self.curr_map and \
                                        generateloc(loc, x, y, -1) in self.curr_map: # xOooo_
                            return 17
                    elif new_loc not in self.curr_map: # Ooo_
                        new_loc = generateloc(loc, x, y, -1)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # oOoo_
                            if generateloc(loc, x, y, -2) in self.curr_map and \
                                    self.curr_map[generateloc(loc, x, y, -2)] == computer: # ooOoo_
                                return 999999
                            if generateloc(loc, x, y, -2) not in self.curr_map: # _oOoo_
                                return 49999
                            else:
                                return 17
                        new_loc = generateloc(loc, x, y, 4)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # Ooo_o
                            if generateloc(loc, x, y, -1) not in self.curr_map:
                                if generateloc(loc, x, y, -2) in self.curr_map and \
                                                self.curr_map[generateloc(loc, x, y, -2)] == computer:
                                    return 49999
                            return 17
                        if generateloc(loc, x, y, -1) not in self.curr_map: # _Ooo_
                            if generateloc(loc, x, y, -2) in self.curr_map and \
                                            self.curr_map[generateloc(loc, x, y, -2)] == computer: # o_Ooo_
                                return 17
                            return 15
                    else: # Ooox
                        new_loc = generateloc(loc, x, y, -1)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # oOoox
                            new_loc = generateloc(loc, x, y, -2)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # ooOoox
                                return 999999
                            return 17
                        elif new_loc not in self.curr_map: # _Ooox
                            new_loc = generateloc(loc, x, y, -2)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # o_Ooox
                                return 17
                            elif new_loc not in self.curr_map:
                                return 1
                elif new_loc in self.curr_map and self.curr_map[new_loc] == computer: # Oox
                    new_loc = generateloc(loc, x, y, -1)
                    if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # oOox
                        new_loc = generateloc(loc, x, y, -2)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # ooOox
                            new_loc = generateloc(loc, x, y, -3)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # oooOox
                                return 999999
                            elif new_loc not in self.curr_map: # _ooOox
                                return 17
                        elif new_loc not in self.curr_map: # _oOox
                            new_loc = generateloc(loc, x, y, -3)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # o_oOox
                                return 17
                            elif new_loc not in self.curr_map:
                                return 1
                    elif new_loc not in self.curr_map: # _Oox
                        if generateloc(loc, x, y, -2) in self.curr_map and \
                            self.curr_map[generateloc(loc, x, y, -2)] == computer: # o_Oox
                            if generateloc(loc, x, y, -3) in self.curr_map and \
                                    self.curr_map[generateloc(loc, x, y, -3)] == computer: # oo_Oox
                                return 17
                            elif generateloc(loc, x, y, -3) not in self.curr_map: # _o_Oox
                                return 1
                else: # Oo_
                    new_loc = generateloc(loc, x, y, -1)
                    if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # oOo_
                        new_loc = generateloc(loc, x, y, -2)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # ooOo_
                            new_loc = generateloc(loc, x, y, -3)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # oooOo_
                                return 999999
                            elif new_loc not in self.curr_map: # _ooOo_
                                return 49999
                            else: # xooOo_
                                return 17
                        elif new_loc not in self.curr_map: # _oOo_
                            new_loc = generateloc(loc, x, y, 3)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # _oOo_o
                                new_loc = generateloc(loc, x, y, -3)
                                if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # o_oOo_o
                                    return 49999
                                return 17
                            new_loc = generateloc(loc, x, y, -3)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # o_oOo_
                                return 17
                            return 15
                        else: # xoOo_
                            new_loc = generateloc(loc, x, y, 3)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # xoOo_o
                                return 17
                            elif new_loc not in self.curr_map: # xoOo__
                                return 1
                    elif new_loc not in self.curr_map: # _Oo_
                        new_loc = generateloc(loc, x, y, -2)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # o_Oo_
                            new_loc = generateloc(loc, x, y, -3)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # oo_Oo_
                                return 17
                            elif new_loc not in self.curr_map: # _o_Oo_
                                return 12
                        new_loc = generateloc(loc, x, y, 3)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # _Oo_o
                            new_loc = generateloc(loc, x, y, 4)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # _Oo_oo
                                return 17
                            elif new_loc not in self.curr_map: # _Oo_o_
                                return 12
                    else: # xOo_
                        new_loc = generateloc(loc, x, y, 3)
                        if new_loc in self.curr_map and self.curr_map[new_loc] == computer: # xOo_o
                            new_loc = generateloc(loc, x, y, 3)
                            if new_loc in self.curr_map and self.curr_map[new_loc] == computer:  # xOo_oo
                                return 17
            return r

        m = -1
        l = tuple()
        for loc in self.poss_locs:
            print(loc)
            t = check_all_directions(loc)
            if t >= 999999:
                return loc
            if m < t:
                m = t
                l = loc
        return l

    def __str__(self):
        return self.curr_map