from scipy.spatial import distance
# For Eye Aspect Ratio
# Left eye aspect ratio
# (161-163) + (157-154) / 2 * (33-133)

# Right eye aspect ratio
# (384-381) + (388-390) / 2 * (362-263)

def ear(eye_array):
    A = distance.euclidean(eye_array[0], eye_array[1])
    B = distance.euclidean(eye_array[2], eye_array[3])
    C = distance.euclidean(eye_array[4], eye_array[5])
    eyeaspectratio = (A + B) / (2.0 * C)
    return eyeaspectratio
