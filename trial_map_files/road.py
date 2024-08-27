import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Define the place of interest (for example, a city or region)
place_name = "Edmonton, Alberta, Canada"  # Change this to your specific location

# Download the road network
G = ox.graph_from_place(place_name, network_type='all')

# Project the graph to UTM for accurate distance measurements
G_proj = ox.project_graph(G)

# Extract nodes and edges with their geographical coordinates
nodes, edges = ox.graph_to_gdfs(G_proj, nodes=True, edges=True)

# Convert nodes and edges to a more accessible format
road_points = {
    "type": "FeatureCollection",
    "features": []
}

for _, row in edges.iterrows():
    coords = list(zip(row['geometry'].xy[1], row['geometry'].xy[0]))
    road_points['features'].append({
        "type": "Feature",
        "properties": {"indoor": False},  # Not indoor
        "geometry": {
            "coordinates": coords,
            "type": "LineString"
        }
    })

# Optionally, save the road_points to a file or use it directly
import json
with open('road_points.json', 'w') as f:
    json.dump(road_points, f, indent=2)

print("Road points have been extracted and saved.")
