

from state import *

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


    def __init__(self, board_size = 11, human_colour = black, computer_colour = white):
        self.board_size = board_size
        self.human_colour = human_colour
        self.computer_colour = computer_colour
        self.curr_state = None

    def startgame(self, who_first):
        mapR, mapI = {}, set()
        self.curr_state = State(self.board_size, mapR, mapI)
        if who_first == human:
            # wait for a listener to give us a place.
            place = (0,0)
            self.human_first_play(place)
            next = computer
        else:
            self.computer_first_play()
            next = human
        self.gaming(next)

    def computer_first_play(self):
        centre = (self.board_size + 1) // 2 - 1
        self.curr_state.first_step((centre, centre), computer)

    def human_first_play(self, place):
        self.curr_state.first_step(place, human)

    def usual_play(self, place, who):
        self.curr_state.new_step(play, who)

    def gaming(self, next): # a recursive call to keep the game move on.
        if next == human:
            # listener tell the place.
            place = (0, 0)
            self.usual_play(place, human)
            ai.human_move(self.curr_state)
            next = computer
        else:
            move = ai.next_move()
            next = human
        self.gaming(next)