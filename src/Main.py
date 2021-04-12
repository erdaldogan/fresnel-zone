import simplekml
from polycircles import polycircles
from utilfunctions import *



def main():
    mef = (29.008578, 41.108460, 200)
    camlica = (29.068520, 41.026062, 265)
    D = haversine(mef[0], mef[1], camlica[0], camlica[1])
    diff = get_diff_angle(mef, camlica)

    kml = simplekml.Kml()
    kml.newpoint(name="MEF University", coords=[mef])  # lon, lat, optional height
    kml.newpoint(name="Camlica Hill", coords=[camlica])  # lon, lat, optional height

    los = kml.newlinestring(name="Line of Sight", description="LOS between given points",
                            coords=[mef, camlica])
    #los.extrude = 1
    los.altitudemode = simplekml.AltitudeMode.absolute
    los.style.linestyle.width = 4
    los.style.linestyle.color = simplekml.Color.pink

    pol = kml.newpolygon(name='A Polygon', altitudemode=simplekml.AltitudeMode.absolute)
    #pol.outerboundaryis = [(29.007434, 41.106582, 100), (29.011761, 41.106916, 100), (29.010320, 41.110875, 100), (29.006149, 41.110221, 100)]
    pol.outerboundaryis = get_circle_coords(mef, 10, diff, 36)
    pol.style.linestyle.color = simplekml.Color.green
    pol.style.linestyle.width = 5
    pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)



    kml.save("fresnel-zone.kml")
if __name__ == "__main__":
    main()
