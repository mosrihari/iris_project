import numpy as np
from scipy.spatial.distance import euclidean

def pixel_width(eye_array, F, W, D):
    pixel = euclidean(eye_array[1], eye_array[0])
    return pixel

def calculate_distance(F, W, P):
    distance = (W * F) / P
    return distance

def focal_length(W, P, D):
    F = (P * D) / W