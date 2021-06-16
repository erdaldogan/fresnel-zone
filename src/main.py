import simplekml
from utilfunctions import *
from geopy.distance import great_circle


def main():

    print("Enter the coordinate A:")
    x = eval(input("Longitude: "))
    y = eval(input("Latitude: "))
    h = eval(input("Height (m): "))
    pointA = (x, y, h)

    print("Enter the coordinate B:")
    x = eval(input("Longitude: "))
    y = eval(input("Latitude: "))
    h = eval(input("Height (m): "))
    pointB = (x, y, h)

    f = eval(input("What is the frequency? (in exp form, 19e6)"))
    # pointA = (29.0484, 41.022, 1780)
    # pointB = (35.334415, 36.995934, 23)
    # pointB = (29.0664, 41.0148, 150)

    distance = sqrt(
        (great_circle(pointA, pointB).m) ** 2 + (pointA[2] - pointB[2]) ** 2)  # great_circle returns 2d distance
    STEP_SIZE = int(distance / 10 + 1)
    ALTITUDE_STEP = (pointA[2] - pointB[2]) / STEP_SIZE
    print("DISTNACE", distance)

    difference = (pointA[0] - pointB[0]), (pointA[1] - pointB[1]), (pointA[2] - pointB[2])

    unit_vector = difference[0] / STEP_SIZE, difference[1] / STEP_SIZE, difference[2] / STEP_SIZE

    # step_coords = unit_vector[0] * step_dist, unit_vector[1] * step_dist, unit_vector[2] * step_dist
    step_coords = unit_vector
    current_point = pointA

    diff = get_diff_angle(pointA, pointB)
    print("DIFF", diff)

    kml = simplekml.Kml()
    kml.newpoint(name="MEF University", coords=[pointA])  # lon, lat, optional height
    kml.newpoint(name="Camlica Hill", coords=[pointB])  # lon, lat, optional height

    los = kml.newlinestring(name="Line of Sight", description="LOS between given points",
                            coords=[pointA, pointB])
    # los.extrude = 1
    los.altitudemode = simplekml.AltitudeMode.absolute
    los.style.linestyle.width = 4
    los.style.linestyle.color = simplekml.Color.red

    for i in range(STEP_SIZE):
        pol = kml.newpolygon(name='A Polygon', altitudemode=simplekml.AltitudeMode.absolute)
        d1 = sqrt((great_circle(pointA, current_point).m) ** 2 + (pointA[2] - current_point[2]) ** 2)
        # print(distance, d1)

        pol.outerboundaryis = get_circle_coords(coord=current_point,
                                                radius=fresnel_radius(1, freq=f, d1=d1, d2=distance - d1),
                                                diff_angle=diff, vertex_no=360)
        pol.style.linestyle.color = simplekml.Color.darkblue
        pol.style.linestyle.width = 5
        pol.style.polystyle.color = simplekml.Color.changealphaint(0, simplekml.Color.rgb(0, 0, 0, 0))
        current_point = current_point[0] - step_coords[0], current_point[1] - step_coords[1], current_point[2] - \
                        ALTITUDE_STEP

    kml.save("fresnel-zone.kml")


if __name__ == "__main__":
    main()
