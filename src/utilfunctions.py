from math import radians, cos, sin, asin, sqrt, pi, atan

c = 3 * 10**8

def haversine(lon1, lat1, h1, lon2, lat2, h2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    d_h = abs(h1 - h2) / 1000
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return sqrt((c * r)**2 + d_h**2) * 1000


def fresnel_radius(n, freq, d1, d2):
    lam = (c) / freq
    return sqrt((n * lam * d1 * d2)/(d1 + d2))


def get_diff_angle(coord1, coord2):
    d_lat = abs(coord1[1] - coord2[1])
    d_lon = abs(coord1[0] - coord2[0])
    return atan((d_lat/d_lon)) * 180/pi  #rad to deg conv


def get_circle_coords(coord, radius, diff, vertex_no):
    lat = coord[0]
    lon = coord[1]
    h = coord[2]
    coord = []
    degree_step = 360.0/vertex_no
    d=0
    while (d <= 360.0):
        delta_lat = sin(d * pi/180) * radius / 111111
        delta_long = 0
        delta_h = cos(d * pi/180) * radius
        coord.append((lat + delta_lat, lon + delta_long, h + delta_h))
        d += degree_step
    return coord

