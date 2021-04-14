import simplekml
from utilfunctions import *



def main():
    STEP_SIZE = 500
    f = 1900 * 10**5
    mef = (29.008578, 41.108460, 180)
    camlica = (29.068520, 41.026062, 265)
    D = haversine(mef[0], mef[1], mef[2], camlica[0], camlica[1], camlica[2])
    diff = get_diff_angle(mef, camlica)

    kml = simplekml.Kml()
    kml.newpoint(name="MEF University", coords=[mef])  # lon, lat, optional height
    kml.newpoint(name="Camlica Hill", coords=[camlica])  # lon, lat, optional height

    los = kml.newlinestring(name="Line of Sight", description="LOS between given points",
                            coords=[mef, camlica])
    #los.extrude = 1
    los.altitudemode = simplekml.AltitudeMode.absolute
    los.style.linestyle.width = 4
    los.style.linestyle.color = simplekml.Color.red

    lat1, lon1 = mef[0], mef[1]
    lat2, lon2 = camlica[0], camlica[1]

    delta_lat = (lat1 - lat2) / STEP_SIZE
    delta_long = (lon1 - lon2) / STEP_SIZE
    delta_h = (mef[2] - camlica[2]) / STEP_SIZE

    tmp = tuple()
    delta_d = haversine(0, 0, 0, delta_long, delta_lat, delta_h)
    for i in range(460):
        tmp = ((delta_lat * i + lat2), (delta_long * i + lon2), (delta_h * i + camlica[2]))
        d1 = delta_d * i
        print(d1)
        pol = kml.newpolygon(name='A Polygon', altitudemode=simplekml.AltitudeMode.absolute)
        pol.outerboundaryis = get_circle_coords(coord=tmp, radius=fresnel_radius(1,freq=f, d1=d1, d2=D-d1),
                                                diff=diff, vertex_no=360)
        pol.style.linestyle.color = simplekml.Color.darkblue
        pol.style.linestyle.width = 5
        pol.style.polystyle.color = simplekml.Color.changealphaint(0, simplekml.Color.rgb(0,0,0,0))

    kml.save("fresnel-zone.kml")
if __name__ == "__main__":
    main()
