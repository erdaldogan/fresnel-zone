import simplekml
from utilfunctions import *
from geopy.distance import great_circle


def main():
    f = 1900 * 10 ** 5

    mef = (29.008578, 41.108460, 80)
    camlica = (29.068520, 41.026062, 270)

    # mef = (29.0484, 41.022, 1780)
    # camlica = (35.334415, 36.995934, 23)
    # camlica = (29.0664, 41.0148, 150)

    distance = sqrt(
        (great_circle(mef, camlica).m) ** 2 + (mef[2] - camlica[2]) ** 2)  # great_circle returns 2d distance
    STEP_SIZE = int(distance / 20 + 1)
    ALTITUDE_STEP = (mef[2] - camlica[2]) / STEP_SIZE
    print("DISTNACE", distance)

    difference = (mef[0] - camlica[0]), (mef[1] - camlica[1]), (mef[2] - camlica[2])

    step_dist = distance / STEP_SIZE
    unit_vector = difference[0] / STEP_SIZE, difference[1] / STEP_SIZE, difference[2] / STEP_SIZE

    # step_coords = unit_vector[0] * step_dist, unit_vector[1] * step_dist, unit_vector[2] * step_dist
    step_coords = unit_vector

    print("STEP DIST", step_dist)
    print("UNIT VECTOR", unit_vector)
    print("STEP COORDS", step_coords)

    current_point = mef

    diff = get_diff_angle(mef, camlica)
    print("DIFF", diff)

    kml = simplekml.Kml()
    kml.newpoint(name="MEF University", coords=[mef])  # lon, lat, optional height
    kml.newpoint(name="Camlica Hill", coords=[camlica])  # lon, lat, optional height

    los = kml.newlinestring(name="Line of Sight", description="LOS between given points",
                            coords=[mef, camlica])
    # los.extrude = 1
    los.altitudemode = simplekml.AltitudeMode.absolute
    los.style.linestyle.width = 4
    los.style.linestyle.color = simplekml.Color.red

    for i in range(STEP_SIZE):
        pol = kml.newpolygon(name='A Polygon', altitudemode=simplekml.AltitudeMode.absolute)
        d1 = sqrt((great_circle(mef, current_point).m) ** 2 + (mef[2] - current_point[2]) ** 2)
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
