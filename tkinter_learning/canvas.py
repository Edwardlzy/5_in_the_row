from tkinter import *

# Get the clicking position and draw the circle.
def getorigin(eventorigin):
      global x,y
      x = eventorigin.x
      y = eventorigin.y
      print(x,y)

      r = 25
      w.create_oval(x-r, y-r, x+r, y+r, fill="black")

master = Tk()
master.bind("<Button 1>", getorigin)

w = Canvas(master, width=1920, height=1080, bg="#FFA23D")
w.pack()

xian = w.create_line(10, 10, 1910, 10)
# w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
w.delete(xian)

w.create_line(0, 225, 1920, 225, width=2)
w.create_line(125, 0, 125, 1080, width=2)
w.create_line(1, 375, 1920, 375, width=2)
w.create_line(325, 0, 325, 1080, width=2)
w.create_oval(100, 200, 150, 250, fill="black")
w.create_oval(300, 350, 350, 400, fill="white")

# w.create_rectangle(50, 25, 150, 75, fill="blue")

mainloop()