import numpy as np

def forward(input_data):
    # Get input dimensions
    num_images, input_height, input_width, num_channels = input_data.shape
    
    # Compute output dimensions
    output_height = input_height // 2
    output_width = input_width // 2
    
    # Initialize output tensor
    output_data = np.zeros((num_images, output_height, output_width, num_channels))
    
    # Iterate over each image in the input data
    for image_idx in range(num_images):
        # Iterate over each channel in the input data
        for channel_idx in range(num_channels):
            # Iterate over each location in the output tensor
            for output_row in range(output_height):
                for output_col in range(output_width):
                    # Compute the maximum value in the 2x2 region
                    max_val = np.max(input_data[image_idx, output_row*2:output_row*2+2, output_col*2:output_col*2+2, channel_idx])
                    output_data[image_idx, output_row, output_col, channel_idx] = max_val
    
    return output_data
