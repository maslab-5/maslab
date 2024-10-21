import numpy as np
import math

def twoNeighbors(corner,corners):
    leftbottom = np.array((0,238))
    print(corners)
    distances = np.linalg.norm(corners-leftbottom, axis=1)
    min_index = np.argmin(distances)
    print(f"the closest point is {corners[min_index]}, at a distance of {distances[min_index]}")
    # distances = np.linalg.norm(corners-corner, axis=1)
    # print(distances)
    # _, min, second_min, *_ = np.partition(distances, 1)
    # min_index, _ = np.where(distances == min)
    # print(f"the closest point is {corners[min_index]}, at a distance of {distances[min_index]}")

def angleThreePoints(vertex,points):
    a = np.array([32.49, -39.96,-3.86])
    b = np.array([31.39, -39.28, -4.66])
    c = np.array([31.14, -38.09,-4.49])

    ba = a - vertex
    bc = c - vertex

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    print (np.degrees(angle))
