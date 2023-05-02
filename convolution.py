import numpy as np

def forward(input_data, num_filters, filter_size):
    # Get input dimensions
    num_images, input_height, input_width, num_channels = input_data.shape

    # Initialize weight and bias parameters
    weights = np.random.randn(filter_size, filter_size, num_channels, num_filters)
    bias = np.zeros(num_filters)

    # Compute output dimensions
    output_height = input_height - filter_size + 1
    output_width = input_width - filter_size + 1

    # Initialize output tensor
    output_data = np.zeros((num_images, output_height, output_width, num_filters))

    # Iterate over each image in the input data
    for image_idx in range(num_images):
        # Iterate over each filter in the convolutional layer
        for filter_idx in range(num_filters):
            # Iterate over each location in the output tensor
            for output_row in range(output_height):
                for output_col in range(output_width):
                    # Compute the dot product of the filter and input tensor
                    dot_product = 0

                    for channel_idx in range(num_channels):
                        for filter_row in range(filter_size):
                            for filter_col in range(filter_size):
                                input_row = output_row + filter_row
                                input_col = output_col + filter_col
                                dot_product += input_data[image_idx, input_row, input_col, channel_idx] * weights[filter_row, filter_col, channel_idx, filter_idx]
                    
                    output_data[image_idx, output_row, output_col, filter_idx] = dot_product + bias[filter_idx]

    # tensor to be rectified
    return output_data

def backward(gradient):
    return