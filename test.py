from tkinter import *

# set up the window
root = Tk()
root.title("Drawing Canvas")

# create the canvas
canvas_width = 800
canvas_height = 600
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# set up the drawing functionality
last_x, last_y = None, None
line_width = 15
line_color = 'black'

def draw(event):
    global last_x, last_y
    if last_x and last_y:
        canvas.create_line(last_x, last_y, event.x, event.y, width=line_width, fill=line_color, capstyle='round')
    last_x, last_y = event.x, event.y

def reset(event):
    global last_x, last_y
    last_x, last_y = None, None

canvas.bind('<B1-Motion>', draw)
canvas.bind('<ButtonRelease-1>', reset)

root.mainloop()
