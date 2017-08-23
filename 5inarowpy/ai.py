# class ai:
#
#
#     def eva_fn(self, state, move):
#         e = 0
#         def one_direction(state, loc, x, y):
#             p, q = loc[0], loc[1]
#             a, b = - 4 * x, - 4 * y
#             i, count = 0, 0
#             while i < 9:
#                 check_loc = (p + a, q + b)
#                 if check_loc in self.curr_map and self.curr_map[check_loc] == who:
#                     count += 1
#                     if count == 5:
#                         return True
#                 else:
#                     count = 0
#                 i, a, b = i+1, a+x, b+y
#             return False
#
#         def check_all_directions(state, loc):
#             for i in range(4):
#                 x, y = [1, 1, 0, -1][i], [1, 0, 1, 1][i]
#                 if one_direction(state, loc, x, y):
#                     return 1
#             return 0
#
#     def next_move(self, state):
#         pass
#
#     def decide(self):
#         pass