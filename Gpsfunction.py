
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

'''from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    return jsonify({'latitude': latitude, 'longitude': longitude})

if __name__ == '__main__':
    app.run()'''
    
