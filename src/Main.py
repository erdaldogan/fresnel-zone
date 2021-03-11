import simplekml
from utilfunctions import haversine, fresnel_radius



def main():
    mef = (29.008578, 41.108460)
    camlica = (29.068520, 41.026062)
    D = haversine(mef[0], mef[1], camlica[0], camlica[1])

    kml = simplekml.Kml()
    kml.newpoint(name="MEF University", coords=[mef])  # lon, lat, optional height
    kml.newpoint(name="Camlica Hill", coords=[camlica])  # lon, lat, optional height

    lin = kml.newlinestring(name="Line of Sight", description="LOS between given points",
                            coords=[mef, camlica])

    kml.save("fresnel-zone.kml")


if __name__ == "__main__":
    main()
