import tkinter as tk
from keras.models import load_model
import numpy as np

# create a window
window = tk.Tk()
window.title("Draw on the grid")

model = load_model('model.h5')

# create a canvas with a 28x28 grid of rectangles
grid_canvas = tk.Canvas(window, width=280, height=280)

for i in range(28):
    for j in range(28):
        x1 = j * 10
        y1 = i * 10
        x2 = x1 + 10
        y2 = y1 + 10
        grid_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

# function to handle mouse movements on the canvas
def draw(event):
    x = event.x // 10
    y = event.y // 10
    if x >= 0 and x < 28 and y >= 0 and y < 28:
        grid_canvas.itemconfig(y * 28 + x + 1, fill="black", outline="black")

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
clear_button = tk.Button(frame, text="Clear Grid", command=lambda: clear_grid())
clear_button.pack(side="left", padx=10)

# create a button to predict the digit
predict_button = tk.Button(frame, text="Predict", command=lambda: predict())
predict_button.pack(side="left", padx=10)

# create a button to close the window
close_button = tk.Button(frame, text="Close", command=window.destroy)
close_button.pack(side="right", padx=10)

# pack the frame in the center of the window
frame.pack(side="top")

# set the size of the window
window.geometry("1152x648")

# function to clear the grid
def clear_grid():
    for i in range(28):
        for j in range(28):
            grid_canvas.itemconfig(i * 28 + j + 1, fill="white",  outline="white")

def predict():
    image = np.zeros((28,28))
    for i in range(28):
        for j in range(28):
            if grid_canvas.itemcget(i * 28 + j + 1, "fill") == "black":
                image[i][j] = 1

    image = image.reshape((1,28,28,1))

    prediction = model.predict(image)

    predicted_digit = np.argmax(prediction)

    print("Predicted:", predicted_digit)

# start the window loop
window.mainloop()
