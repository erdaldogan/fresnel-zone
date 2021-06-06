from math import radians, cos, sin, asin, sqrt, pi, atan2

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
    d_lon = abs(coord2[0] - coord1[0])
    y = sin(d_lon) * cos(coord2[1])
    x = cos(coord1[1]) * sin(coord2[1]) - sin(coord1[1]) * cos(coord2[1]) * cos(d_lon)
    return atan2(y, x) * 180.0/pi  #rad to deg conv

def rotate_point(point, origin, angle):
    angle_rad = angle * pi/180.0
    (px, py) = point
    (ox, oy, _) = origin
    x = cos(angle_rad) * (px - ox) - sin(angle_rad) * (py - oy) + ox
    y = sin(angle_rad) * (px - ox) + cos(angle_rad) * (py - oy) + oy
    return x, y


def get_circle_coords(coord, radius, diff_angle, vertex_no):
    lat = coord[0]
    lon = coord[1]
    h = coord[2]
    coord_out = []
    degree_step = 360.0/vertex_no
    d=0
    # long = horizontal
    # lat = vertical
    while d <= 360.0:
        delta_lat = sin(d * pi/180) * radius / 111111
        delta_long = 0
        delta_h = cos(d * pi/180) * radius
        (x, y) = rotate_point(point=(lat + delta_lat, lon + delta_long),
                          origin=coord, angle=diff_angle)
        coord_out.append((x, y, h + delta_h))
        #coord_out.append((lat + delta_lat, lon + delta_long, h + delta_h))

        d += degree_step
    return coord_out

