from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()

	# Creation of init_window
	def init_window(self):
		# Change the title of the master widget.
		self.master.title("GUI")

		# Allowing the widget to take the full space of the root window.
		self.pack(fill=BOTH, expand=1)

		# Define a button object.
		# quitButton = Button(self, text="Quit", command=self.client_exit)
		# # Placing the button on my window.
		# quitButton.place(x=0, y=0)

		# Creating a menu bar.
		menu = Menu(self.master)
		self.master.config(menu=menu)

		# Creating a file menu.
		file = Menu(menu)
		# Add a command to the menu option.
		file.add_command(label="Exit", command=self.client_exit)
		# Add the file menu under the menu bar.
		menu.add_cascade(label="File", menu=file)

		# Create an edit menu.
		edit = Menu(menu)
		edit.add_command(label="Undo")
		edit.add_command(label="Show Image", command=self.show_image)
		edit.add_command(label="Show Text", command=self.show_text)
		menu.add_cascade(label="Edit", menu=edit)

	def client_exit(self):
		exit()

	# Resize an image to fit the current window size.
	def resize_image(self, img_w, img_h, window_w, window_h, image):
		w_ratio = window_w / img_w
		h_ratio = window_h / img_h
		ratio = min(w_ratio, h_ratio)

		w = int(img_w * ratio)
		h = int(img_h * ratio)
		return image.resize((w, h), Image.ANTIALIAS)

	def show_image(self):
		load = Image.open("yanye.jpg")
		# Get the size of the image.
		w, h = load.size

		window_h = self.master.winfo_height()
		window_w = self.master.winfo_width()

		load_resized = self.resize_image(w, h, window_w, window_h, load)
		render = ImageTk.PhotoImage(load_resized)

		# Labels can be texts or images.
		img = Label(self, image=render, width=window_w, height=window_h)
		img.pack(fill=BOTH, expand=1)
		img.image = render
		img.place(x=0, y=0)

	def show_text(self):
		text = Label(self, text="Hello world!")
		text.pack()

root = Tk()

# Size of the window.
root.geometry("1920x1080")
app = Window(root)

# Bring up the window.
root.mainloop()