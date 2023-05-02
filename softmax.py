import numpy as np

def forward(x):
    # Compute the exponential of each element in the input array
    exp_x = np.exp(x)

    # Sum the exponential values across each row
    sum_exp_x = np.sum(exp_x, axis=1, keepdims=True)

    # Compute the softmax probabilities for each element in the input array
    softmax_probs = exp_x / sum_exp_x

    return softmax_probs
