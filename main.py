import tkinter as tk
import numpy as np
from PIL import ImageGrab, ImageOps, Image
from keras.models import load_model
import tkinter.ttk as ttk
from tkinter.ttk import Style
import os
import sys

# change dir
path = getattr(sys, '_MEIPASS', os.getcwd())   
os.chdir(path)

# Load the model
model = load_model('assets\model.h5')
icon = 'assets\code.ico'

# set up the window
root = tk.Tk()
root.title("MNIST Number Recognition")

root.iconbitmap(icon)

root.style = Style()
root.style.theme_use("clam")
root.configure(background=root.style.lookup("TFrame", "background"))

# create the canvas
canvas_width = 600
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
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

def clear_canvas():
    output_digit.set(" ")
    canvas.delete("all")

def calculate_canvas_pixel_value(canvas):
    # Get the bounding box of the canvas
    x = canvas.winfo_rootx() + canvas.winfo_x()
    y = canvas.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    # Capture the image of the canvas
    img = ImageGrab.grab(bbox=(x, y, x1, y1))

    # Calculate the total pixel value of the image
    pixel_value = np.sum(np.array(img.convert('L'))) / (canvas.winfo_width() * canvas.winfo_height())

    return pixel_value

def predict():
    # Calculate the pixel value of the canvas
    pixel_value = calculate_canvas_pixel_value(canvas)

    # If the pixel value is below the threshold, assume that no digit has been drawn
    if pixel_value > 252:
        output_digit.set("<N/A>")
        return
    
    # Get the image from the canvas
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    img = ImageGrab.grab((x, y, x1, y1)).convert('L')
    
    # Resize the image to 28x28 pixels
    img = img.resize((28, 28))
    
    # Normalize the pixel values
    img = ImageOps.invert(img)
    img = np.array(img) / 255.0
    
    # Reshape the image into a 4D array (batch size, height, width, channels)
    img = img.reshape((1, 28, 28, 1))
    
    # Make a prediction using the model
    prediction = model.predict(img, verbose = 0)

    digit = np.argmax(prediction)

    output_digit.set(str(digit))

# create the clear button
clear_button = ttk.Button(root, text="Clear Canvas", command=clear_canvas, takefocus=False)
clear_button.pack(side='left', padx=10, pady=10)

# Add the Predict button
predict_button = ttk.Button(root, text="Predict", command=predict, takefocus=False)
predict_button.pack(side='left', padx=10, pady=10)

# setup output text
output = tk.StringVar()
output.set("You drew a: ")

output_label = tk.Label(root, textvariable=output, font=('', 15), bg='#d9d9d9')
output_label.pack(side='left', padx=10, pady=10)

output_digit = tk.StringVar()
output_digit.set(" ")

output_digit_label = tk.Label(root, textvariable=output_digit, font=('', 15), bg='white', fg='black', width=5, height=1)
output_digit_label.pack(side='left', padx=10, pady=10)

# Bind the mouse events to the canvas
canvas.bind('<B1-Motion>', draw)
canvas.bind('<ButtonRelease-1>', reset)

root.mainloop()
