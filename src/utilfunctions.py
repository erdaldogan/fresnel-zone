from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def fresnel_radius(n, freq, d1, d2):
    return sqrt((n * freq * d1 * d2)/(d1 + d2))


def get_circle_coords(coord, radius, tilt, vertex_no):
    lat = coord[0]
    lon = coord[1]
    coord = []
    degree_step = 360.0/vertex_no
    d=0
    while (d < 360.0):
        delta_x = sin(d) * radius
        delta_y = radius * cos(d)
        coord.append((lat + delta_x, lon + delta_y))
        d += degree_step
    return coord

