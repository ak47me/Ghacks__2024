


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    return jsonify({'latitude': latitude, 'longitude': longitude})

if __name__ == '__main__':
    app.run()
    
