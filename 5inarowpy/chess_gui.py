from tkinter import *
from state import *

class Window(Frame):
	def __init__(self, master=None, turn=1, size=15, depth=1):
	# def __init__(self, master=None, size=15):
		Frame.__init__(self, master)
		self.master = master
		self.canvas = Canvas(self.master, width=720, height=720, bg="#FFA23D")
		self.canvas.pack()
		self.turn = turn
		self.steps = []
		self.size = size
		self.sep_len = (720 - 30 - 30) / (self.size - 1)
		self.bitmap = {}
		self.custom_init()
		self.curr_state = State(15, {}, set())
		self.step = 0
		self.his = []
		self.depth = depth


	# A helper to analyze the clicking location. Return the index on 
	# board of the step.
	def get_clicking_loc(self, event):
		# Actual position.
		x = event.x
		y = event.y

		if (x < 0 or y < 0 or x >=710 or y >= 710):
			# print("Invalid position!")
			return

		# Position on the board.
		x_temp = (x - 30) / self.sep_len
		x_index = int(x_temp) + 1 if (x_temp - int(x_temp) >= 0.5) else int(x_temp)
		y_temp = (y - 30) / self.sep_len
		y_index = int(y_temp) + 1 if (y_temp - int(y_temp) >= 0.5) else int(y_temp)

		x = 30 + x_index * self.sep_len
		y = 30 + y_index * self.sep_len
		# print("position: (", x, ", ", y, ")")
		if self.draw_chess(x, y):
			self.bitmap[(x, y)] = 1
			self.curr_state.new_step((x_index, y_index), 1)
			self.his.append(self.curr_state.copy())
			# loc = self.curr_state.eva_fn()
			loc = self.curr_state.minimaxFn(self.depth)
			print(loc)
			x, y = 30 + loc[0] * self.sep_len, 30 + loc[1] * self.sep_len
			self.draw_chess(x, y)
			self.curr_state.new_step(loc, 0)
			self.his.append(self.curr_state.copy())
			self.bitmap[(x, y)] = 1
		# print("position:", x_index, y_index)
			return x_index, y_index


	# Build the window and necessary settings.
	def custom_init(self):
		self.master.title("5 in a row")
		self.pack(fill=BOTH, expand=True)

		# Create a menu bar.
		menu_bar = Menu(self.master)
		self.master.config(menu=menu_bar)

		# Add a play menu.
		play = Menu(menu_bar)
		play.add_command(label="start a new game", command=self.restart)
		play.add_command(label="reverse one step", command=self.reverse)
		menu_bar.add_cascade(label="play", menu=play)
		self.draw_board()
		self.canvas.bind("<Button 1>", self.get_clicking_loc)


	# Draw the play board.
	def draw_board(self):
		side_len = 720 - 30 - 30

		# Draw the four border lines.
		self.canvas.create_line(30, 30, 690, 30, width=3)
		self.canvas.create_line(30, 30, 30, 690, width=3)
		self.canvas.create_line(30, 690, 690, 690, width=3)
		self.canvas.create_line(690, 30, 690, 690, width=3)

		curr_pos = 30 + self.sep_len

		# Draw the remaining lines and store the position.
		for i in range(self.size - 1):
			self.canvas.create_line(30, curr_pos, 690, curr_pos, width=2)
			self.canvas.create_line(curr_pos, 30, curr_pos, 690, width=2)
			curr_pos += self.sep_len

		# Draw 5 supporting dots.
		self.canvas.create_oval(720/2-6, 720/2-6, 720/2+5, 720/2+5, fill="black")
		top = 30 + 3 * self.sep_len
		bot = 720 - 30 - 3 * self.sep_len
		self.canvas.create_oval(top-6, top-6, top+5, top+5, fill="black")
		self.canvas.create_oval(bot-6, top-6, bot+5, top+5, fill="black")
		self.canvas.create_oval(top-6, bot-6, top+5, bot+5, fill="black")
		self.canvas.create_oval(bot-6, bot-6, bot+5, bot+5, fill="black")


	# Display the latest chess choice.
	def draw_chess(self, x, y):
		if ((x, y) in self.bitmap and self.bitmap[(x, y)] == 1):
			return 0
		# Update records for reverse use.

		if (self.turn == 0):
			self.steps.append(((x, y), self.canvas.create_oval(x-17, y-17, x+17, y+17, fill="white")))
		else:
			self.steps.append(((x, y), self.canvas.create_oval(x-17, y-17, x+17, y+17, fill="black")))
		self.turn = 1 - self.turn
		return 1
		# print("position: (", x, ", ", y, ")")
		# self.steps.append(((x, y), self.canvas.create_oval(x - 17, y - 17, x + 17, y + 17, fill="black")))
		# self.curr_state.new_step((x, y), 1)
		# self.his.append(self.curr_state.copy())
		# loc = self.curr_state.eva_fn()
		# self.steps.append((loc, self.canvas.create_oval(x - 17, y - 17, x + 17, y + 17, fill="white")))
		# self.curr_state.new_step(loc, 0)
		# self.his.append(self.curr_state.copy())



	# A method to reverse one step back.
	def reverse(self):
		try:
			step = self.steps.pop(-1)
			self.canvas.delete(step[1])
			self.bitmap[step[0]] = 0
			self.his.pop(-1)
		except:
			return
		try:
			step = self.steps.pop(-1)
			self.canvas.delete(step[1])
			self.bitmap[step[0]] = 0
			self.his.pop(-1)
			self.curr_state = self.his[-1].copy()
		except:
			return
		# self.turn = 1 - self.turn


	# Restart the game.
	def restart(self):
		for item in self.bitmap:
			self.reverse()
		self.his = []
		self.curr_state = State(15, {}, set())


root = Tk()
root.geometry("720x720")
app = Window(root)
print(app.steps)
print(app.his)
root.mainloop()
