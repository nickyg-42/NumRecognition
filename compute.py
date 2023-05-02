from keras.datasets import mnist
import numpy as np
import convolution as conv
import relu
import max_pool
import flatten
import fully_connected as fc
import softmax

# load MNIST image data into tuples
(train_input, train_output), (test_input, test_output) = mnist.load_data()

# normalize input data by transforming from grayscale to B&W
train_input /= 255.0
test_input /= 255.0

batch_size = 32
batches = len(train_input)

epochs = 10

learning_rate = .01

# loss helper
def calculate_loss(probabilities, labels):
    # Calculate cross-entropy loss
    loss = np.sum(-np.log(probabilities) * labels) / len(labels)
    return loss

# gradient helper
def calculate_gradient(output, label):
    # Calculate the derivative of cross-entropy loss with respect to the output
    d_loss = output - label
    return d_loss

for i in range(epochs):
    for j in range(batches):
        batch_input = train_input[j*batch_size:(j+1)*batch_size]
        batch_output = train_output[j*batch_size:(j+1)*batch_size]

        # convolute
        convolution_output = conv.forward(batch_input, 32, 3)
        # RelU
        relu_output = relu.relu(convolution_output)
        # pool
        pool_output = max_pool.forward(relu_output)
        # flatten
        flattened = flatten.forward(pool_output)
        # fc
        fully_connected = fc.forward(flattened)
        # softmax
        probabilities = softmax.forward(fully_connected)

        loss = calculate_loss(probabilities, batch_output)
        gradient = calculate_gradient(probabilities, batch_output)

        # backpropagate
        gradient = softmax.backward(gradient)

        gradient = fc.backward(gradient)

        gradient = flatten.backward(gradient)

        gradient = max_pool.backward(gradient)

        gradient = conv.backward(gradient)

        # update weights and biases
        conv.update_params(learning_rate)
        fc.update_params(learning_rate)

