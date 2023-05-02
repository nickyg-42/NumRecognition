import numpy as np

def forward(pool_output):
    # Get input dimensions
    num_images, input_height, input_width, num_channels = pool_output.shape

    # Compute output dimension
    output_size = input_height * input_width * num_channels

    # Reshape input data to a 2D matrix
    flattened_input = np.reshape(pool_output, (num_images, output_size))

    return flattened_input
