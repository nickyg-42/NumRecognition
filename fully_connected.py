import numpy as np
import relu

def forward(input_data, num_neurons):
    # Get input dimensions
    input_size = input_data.shape[1]

    # Initialize weight and bias parameters
    weights = np.random.randn(input_size, num_neurons)
    bias = np.zeros(num_neurons)

    # Compute dot product of input and weights, and add bias
    output_data = np.dot(input_data, weights) + bias

    # ReLU activation
    return relu.relu(output_data)

