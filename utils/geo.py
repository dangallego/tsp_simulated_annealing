import numpy as np

"""
Geographic utility functions for computing great-circle distances
and building distance matrices based on latitude/longitude pairs.
"""

def great_circle_distance(coord1, coord2, R=6371):
    """
    Computes the great-circle distance between two points on the Earth's surface
    using the spherical law of cosines and unit vectors.

    Parameters:
        coord1 (tuple): (latitude, longitude) of the first city in degrees.
        coord2 (tuple): (latitude, longitude) of the second city in degrees.
        R (float): Radius of the Earth in kilometers. Default is 6371 km.

    Returns:
        float: Great-circle distance in kilometers between the two coordinates.
    """
    # Convert lat/lon from degrees to radians
    phi1, lambda1 = np.radians(coord1)
    phi2, lambda2 = np.radians(coord2)

    # Convert both points to 3D unit vectors
    u1 = np.array([
        np.cos(phi1) * np.cos(lambda1),
        np.cos(phi1) * np.sin(lambda1),
        np.sin(phi1)
    ])
    u2 = np.array([
        np.cos(phi2) * np.cos(lambda2),
        np.cos(phi2) * np.sin(lambda2),
        np.sin(phi2)
    ])

    # Compute arc cosine of dot product (clipped to avoid numerical error)
    return R * np.arccos(np.clip(np.dot(u1, u2), -1.0, 1.0))


def compute_distance_matrix(city_coords):
    """
    Computes a symmetric distance matrix for a list of cities given their coordinates.

    Parameters:
        city_coords (list of tuples): List of (latitude, longitude) for each city.

    Returns:
        np.ndarray: 2D array of pairwise great-circle distances between cities.
    """
    n = len(city_coords)
    D = np.zeros((n, n))

    # Fill only the upper triangle of the matrix and mirror it
    for i in range(n):
        for j in range(i + 1, n):
            distance = great_circle_distance(city_coords[i], city_coords[j])
            D[i][j] = distance
            D[j][i] = distance  # Symmetric matrix

    return D
