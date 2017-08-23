from state import *
# from ai import *

computer = 0
human = 1

black = 0
white = 1
green = 2
grey = 3
red = 4
orange = 5
yellow = 6
blue = 7
pink = 8
purple = 9


class play:


    def __init__(self, board_size = 15, human_colour = black, computer_colour = white):
        self.board_size = board_size # only accept odd size to enable a centre.
        self.human_colour = human_colour
        self.computer_colour = computer_colour
        self.curr_state = None

    def startgame(self, who_first):
        mapR, mapI = {}, set()
        self.curr_state = State(self.board_size, mapR, mapI)
        if who_first == human:
            # wait for a listener to give us a place.
            place = (0,0) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.curr_state.new_step(place, human)
            next = computer
        else:
            centre = self.board_size // 2
            self.curr_state.new_step((centre, centre), computer)
            next = human
        self.gaming(next)

    def usual_play(self, place, who):
        self.curr_state.new_step(play, who)

    def gaming(self, next): # a recursive call to keep the game move on.
        if next == human:
            # listener tell the place.
            place = (0, 0) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.usual_play(place, human)
            next = computer
        else:
            move = self.curr_state.eva_fn()
            self.usual_play(move, computer)
            next = human
        self.gaming(next)