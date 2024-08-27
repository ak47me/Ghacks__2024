
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import networkx as nx
from geopy.distance import geodesic
from gps3 import gps3
from geopy.geocoders import Nominatim



# Sample points data (replace with your actual data)
points = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"indoor": True},
            "geometry": {
                "coordinates": [
                    [
                        -113.52861715675292,
                        53.5274560962425
                    ],
                    [
                        -113.52947268343289,
                        53.5270633116958
                    ],
                    [
                        -113.5292436497477,
                        53.52677641694743
                    ],
                    [
                        -113.52919518558801,
                        53.52630365610955
                    ],
                    [
                        -113.5292011164582,
                        53.52615295141294
                    ],
                    [
                        -113.5289674759043,
                        53.526017015893274
                    ],
                    [
                        -113.5286723489005,
                        53.52600987148793
                    ],
                    [
                        -113.5280078213777,
                        53.52585815067917
                    ],
                    [
                        -113.52789939835228,
                        53.52561962974693
                    ],
                    [
            -113.52881872572137,
            53.52803974502379
          ],
          [
            -113.52822105030269,
            53.52808960324154
          ],
          [
            -113.52823319823538,
            53.52790649230084
          ],
          [
            -113.5284234732593,
            53.5275337468716
          ],
          [
            -113.52861567388092,
            53.52745458624986
          ],
          [
            -113.52468510363698,
            53.52801366019719
          ],
          [
            -113.52467764879222,
            53.527825518615174
          ],
          [
            -113.5247511684419,
            53.526814717886765
          ],
          [
            -113.52450734164086,
            53.52674439556546
          ],
          [
            -113.52409004721467,
            53.526742269542865
          ],
          [
            -113.52473555175418,
            53.52681584835469
          ],
          [
            -113.52476452105294,
            53.52631004052404
          ],
          [
            -113.52475023942844,
            53.52610393051327
          ],
          [
            -113.52475048203785,
            53.525224730853665
          ],
          [
            -113.52418680396167,
            53.5252402132875
          ],
          [
            -113.52342486364886,
            53.525154604784404
          ],
          [
            -113.52122330232613,
            53.52494706923602
          ],
          [
            -113.52112226433717,
            53.52501731301615
          ],
          [
            -113.52096204679965,
            53.52503246367982
          ],
          [
            -113.52071712193965,
            53.52490028467787
          ],
          [
            -113.52033483662629,
            53.5247020522643
          ],
          [
            -113.52095738583117,
            53.5250331240523
          ],
          [
            -113.52098125090018,
            53.525962074485165
          ],
          [
            -113.52115498757767,
            53.52596582996094
          ],
          [
            -113.52098801353398,
            53.525969403231386
          ],
          [
            -113.52072292122303,
            53.526713944343385
          ],
          [
            -113.52076397606781,
            53.52737850441619
          ],
          [
            -113.52032070333752,
            53.52733463439736
          ],
          [
            -113.52075741471404,
            53.527378897484795
          ],
          [
            -113.5209853529522,
            53.52737286598364
          ],
          [
            -113.52125792596907,
            53.52747712649301
          ],
          [
            -113.5220684124643,
            53.5278828275045
          ],

                ],
                "type": "LineString"
            }
        }
    ]
}

def create_graph():
    G = nx.Graph()
    for feature in points['features']:
        coords = feature['geometry']['coordinates']
        indoor = feature['properties'].get('indoor', False)
        for i in range(len(coords) - 1):
            pos_A = (coords[i][1], coords[i][0])
            pos_B = (coords[i + 1][1], coords[i + 1][0])
            G.add_node(f'Node_{i}', pos=pos_A)
            G.add_node(f'Node_{i + 1}', pos=pos_B)
            distance = geodesic(pos_A, pos_B).meters
            weight = distance if indoor else distance * 1.5
            G.add_edge(f'Node_{i}', f'Node_{i + 1}', weight=weight, indoor=indoor)
    return G

def find_nearest_node(graph, lat, lon):
    pos = nx.get_node_attributes(graph, 'pos')
    min_dist = float('inf')
    nearest_node = None
    for node, (node_lat, node_lon) in pos.items():
        dist = geodesic((lat, lon), (node_lat, node_lon)).meters
        if dist < min_dist:
            min_dist = dist
            nearest_node = node
    return nearest_node

def required_points(start_coords, end_coords):
    G = create_graph()
    start_node = find_nearest_node(G, *start_coords)
    end_node = find_nearest_node(G, *end_coords)
    G.add_node('start', pos=start_coords)
    G.add_node('end', pos=end_coords)
    pos = nx.get_node_attributes(G, 'pos')
    pos['start'] = start_coords
    pos['end'] = end_coords
    start_distance = geodesic(start_coords, pos[start_node]).meters
    end_distance = geodesic(end_coords, pos[end_node]).meters
    G.add_edge('start', start_node, weight=start_distance)
    G.add_edge('end', end_node, weight=end_distance)
    shortest_path = nx.shortest_path(G, source='start', target='end', weight='weight')
    path_coords = [pos[node] for node in shortest_path]
    return path_coords


def get_lat_long(start):
    loc = Nominatim(user_agent="Geopy Library")
    getLoc1 = loc.geocode(start)
    if getLoc1:
        return {"latitude": getLoc1.latitude, "longitude": getLoc1.longitude}
    else:
        print("Location not found")
        return None


start_coords = (53.528206598119596, -113.52927950143817)
end_coords = (53.528204362561894, -113.52135165224719)

# Get the path coordinates
all_points = required_points(start_coords, end_coords)

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/coordinates/start', methods=['GET'])
def get_coordinates_start():
    return jsonify({
        'start': all_points[0],
        'end': all_points[1]
    })

@app.route('/api/coordinates/end', methods=['GET'])
def get_coordinates_end():
    return jsonify({
        'start': all_points[-2],
        'end': all_points[-1]
    })

@app.route('/api/path', methods=['GET'])
def get_path():
    return jsonify({
        "path": all_points[1: -1]
    })

@app.route('/api/coordinates', methods=['POST'])
def receive_coordinates():
    data = request.json
    start = data.get("start")
    end = data.get("end")
    start_coord = get_lat_long(start)
    end_coord = get_lat_long(end)
    latitude1 = start_coord["latitude"]
    longitude1 = start_coord["longitude"]
    latitude2 = end_coord["latitude"]
    longitude2 = end_coord["longitude"]

    
    # Recalculate the path using the new coordinates
    start_coords = (latitude1, longitude1)
    end_coords = (latitude2, longitude2)
    global all_points
    all_points = required_points(start_coords, end_coords)
    
    # Return the recalculated path
    return jsonify({
        'start': start_coords,
        'end': end_coords,
        'path': all_points
    })

if __name__ == '__main__':
    # Initialize with default coordinates
    start_coords = (53.528206598119596, -113.52927950143817)
    end_coords = (53.528204362561894, -113.52135165224719)
    all_points = required_points(start_coords, end_coords)
    
    app.run(debug=True)