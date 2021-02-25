import numpy as np



def dict_to_np_array(x):
    return np.array([x['x'], x['y']])


def get_angle(a, b, c):

    A, B, C = list(map(dict_to_np_array, [a,b,c]))

    BA = A - B
    BC = C - B

    cosine_angle = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))
    
    angle = np.arccos(cosine_angle)
    angle = np.degrees(angle)

    return angle