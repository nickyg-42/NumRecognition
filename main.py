import tkinter as tk
from keras.models import load_model
import numpy as np
import tkinter.ttk as ttk
from PIL import Image
import math

# create a window
window = tk.Tk()
window.title("Draw on the grid")
window.iconbitmap('code.ico')

model = load_model('model.h5')

# create a canvas with a 28x28 grid of rectangles
grid_canvas = tk.Canvas(window, width=560, height=560)

for i in range(56):
    for j in range(56):
        x1 = j * 10
        y1 = i * 10
        x2 = x1 + 10
        y2 = y1 + 10
        grid_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

# function to handle mouse movements on the canvas
def draw(event):
    x = math.floor(event.x * 56 / 560)
    y = math.floor(event.y * 56 / 560)
    if x >= 0 and x < 56 and y >= 0 and y < 56:
        grid_canvas.itemconfig(y * 56 + x + 1, fill="black", outline="black")


# bind the canvas to the draw function for mouse movement
grid_canvas.bind("<B1-Motion>", draw)

# pack the grid canvas in the center of the window
grid_canvas.pack(side="top", padx=20, pady=20)

# create a frame to hold the buttons
frame = tk.Frame(window)

# create a label for instructions
label = tk.Label(frame, text="Draw on the grid using your mouse", font=("Arial", 14))
label.pack(side="top", pady=10)

# create a button to clear the grid
clear_button = ttk.Button(frame, text="Clear Grid", command=lambda: clear_grid())
clear_button.pack(side="left", padx=10)

# create a button to predict the digit
predict_button = ttk.Button(frame, text="Predict", command=lambda: predict())
predict_button.pack(side="left", padx=10)

# create a button to close the window
close_button = ttk.Button(frame, text="Close", command=window.destroy)
close_button.pack(side="right", padx=10)

# pack the frame in the center of the window
frame.pack(side="top")

# set the size of the window
window.geometry("1500x800")

# function to clear the grid
def clear_grid():
    for i in range(56):
        for j in range(56):
            grid_canvas.itemconfig(i * 56 + j + 1, fill="white",  outline="white")

def predict():
    image = np.zeros((56,56))
    for i in range(56):
        for j in range(56):
            if grid_canvas.itemcget(i * 56 + j + 1, "fill") == "black":
                image[i][j] = 1

    image = Image.fromarray(image)
    image = image.resize((28, 28))
    image = np.array(image)
    image = image.reshape((1, 28, 28, 1))

    prediction = model.predict(image)

    predicted_digit = np.argmax(prediction)

    print("Predicted:", predicted_digit)

# start the window loop
window.mainloop()
