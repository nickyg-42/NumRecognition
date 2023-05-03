import tkinter as tk
import numpy as np
from PIL import ImageGrab, ImageOps
from keras.models import load_model
import tkinter.ttk as ttk

# Load the saved model
model = load_model('model.h5')

# set up the window
root = tk.Tk()
root.title("Drawing Canvas")

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
    canvas.delete("all")

def predict():
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
    prediction = model.predict(img)

    digit = np.argmax(prediction)

    print("Predicted:", digit)

# create the clear button
clear_button = ttk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_button.pack(side='left', padx=10, pady=10)

# Add the Predict button
predict_button = ttk.Button(root, text="Predict", command=predict)
predict_button.pack(side='left', padx=10, pady=10)

# Bind the mouse events to the canvas
canvas.bind('<B1-Motion>', draw)
canvas.bind('<ButtonRelease-1>', reset)

root.mainloop()
