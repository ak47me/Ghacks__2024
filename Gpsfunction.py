
import gps
def gpsmkbsdk():
    session = gps.gps(mode=gps.WATCH_ENABLE)
    while True:
        try:
            report = session.next()
            if report['class'] == 'TPV':
                if hasattr(report, 'lat') and hasattr(report, 'lon'):
                    return (report.lat, report.lon)
        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
coords = get_gps_coordinates()
print(f"Coordinates: {coords}")