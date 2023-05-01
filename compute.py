from keras.datasets import mnist
import convolution as cv

# load MNIST image data into tuples
(train_input, train_output), (test_input, test_output) = mnist.load_data()

# normalize input data by transforming from grayscale to B&W
train_input /= 255.0
test_input /= 255.0

