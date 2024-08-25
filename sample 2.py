import requests
import folium
import os
from typing import Tuple, List

# Replace with your Mapbox access token
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiYW1rMjM3IiwiYSI6ImNtMDhnNGhpazFkaHoycXB2Ync0bjc0ajcifQ.Nt_jrgNlhvQ1XOgIgZtCNw'

# Predefined coordinates
coordinates = [
    [
        [53.52501394756737, -113.52122913673706],
        [53.52501714929542, -113.52072060360172],
        [53.52749981891861, -113.52076956461727],
        [53.52748874336393, -113.52245999968656],
        [53.52774166970113, -113.52250118998037],
        [53.52776674936845, -113.52180141396458],
        [53.52819492073496, -113.52144016207536]
    ],
    [
        [53.525052546950235, -113.52119314300249],
        [53.525070166653734, -113.52084274146328],
        [53.52612218349765, -113.52086135334153],
        [53.526096222561335, -113.52153658827574]
    ],
    [
        [53.52500376534286, -113.52366013697306],
        [53.52545758339812, -113.52348994765711],
        [53.52524104516334, -113.52420143423929],
        [53.52524724666702, -113.52473891745484],
        [53.52556226497205, -113.52471219465674],
        [53.52602161305447, -113.524719215875],
        [53.52601851366529, -113.5240203595364],
        [53.52605431729208, -113.52348938972247]
    ],
    [
        [53.526019256057026, -113.52472183316128],
        
    ]
]

# Function to validate user input
def validate_input(location: str) -> str:
    """
    Validate user input for the location. Ensures input is not empty and checks for a valid format.
    """
    if not location.strip():
        raise ValueError("Location cannot be empty.")
    return location.strip()

# Function to get coordinates using Mapbox Geocoding API
def get_coordinates(location: str) -> Tuple[float, float]:
    """
    Get the latitude and longitude of a location using the Mapbox Geocoding API.
    """
    try:
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json'
        params = {'access_token': MAPBOX_ACCESS_TOKEN, 'limit': 1}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if not data['features']:
            raise ValueError(f"Location '{location}' not found.")
        
        lon, lat = data['features'][0]['geometry']['coordinates']
        return lat, lon

    except requests.exceptions.ConnectionError:
        raise ConnectionError("Failed to connect to the Mapbox API. Please check your network connection.")
    except requests.exceptions.Timeout:
        raise TimeoutError("Request to the Mapbox API timed out.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred while fetching geocoding data: {e}")

# Function to get directions using Mapbox Directions API
def get_directions(start_coords: Tuple[float, float], end_coords: Tuple[float, float], predefined_waypoints: List[List[Tuple[float, float]]]) -> List[Tuple[float, float]]:
    """
    Get the driving directions between two locations using the Mapbox Directions API, with predefined waypoints.
    """
    try:
        url = 'https://api.mapbox.com/directions/v5/mapbox/driving'
        params = {
            'access_token': MAPBOX_ACCESS_TOKEN,
            'geometries': 'geojson',  # Get route geometry in GeoJSON format
            'overview': 'full',
            'alternatives': 'false'
        }
        
        # Convert the coordinates into a string format required by the API
        coords = f"{start_coords[1]},{start_coords[0]}"  # Start point
        for waypoint_set in predefined_waypoints:
            for waypoint in waypoint_set:
                coords += f";{waypoint[1]},{waypoint[0]}"  # Add waypoints
        coords += f";{end_coords[1]},{end_coords[0]}"  # End point
        
        # Make the API request
        response = requests.get(f'{url}/{coords}', params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if 'routes' not in data or not data['routes']:
            raise ValueError("No route found.")

        route_geometry = data['routes'][0]['geometry']['coordinates']
        return [(lat, lon) for lon, lat in route_geometry]  # Reverse coordinates to lat, lon

    except requests.exceptions.ConnectionError:
        raise ConnectionError("Failed to connect to the Mapbox API. Please check your network connection.")
    except requests.exceptions.Timeout:
        raise TimeoutError("Request to the Mapbox API timed out.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred while fetching directions: {e}")

# Function to create a map and plot directions
def create_map(start_location: str, end_location: str) -> None:
    """
    Create a Folium map with directions between the start and end locations using predefined waypoints.
    """
    try:
        start_coords = get_coordinates(start_location)
        end_coords = get_coordinates(end_location)
        route = get_directions(start_coords, end_coords, coordinates)

        # Create a folium map centered at the start location
        map_obj = folium.Map(location=start_coords, zoom_start=13)

        # Add markers for the start and end locations
        folium.Marker(start_coords, popup=f"Start: {start_location}").add_to(map_obj)
        folium.Marker(end_coords, popup=f"End: {end_location}").add_to(map_obj)

        # Add a polyline to the map to show the route
        folium.PolyLine(route, color="blue", weight=5, opacity=0.7).add_to(map_obj)

        # Save the map to an HTML file
        file_name = "mapbox_directions_with_predefined_waypoints_map.html"
        if os.path.exists(file_name):
            print(f"File '{file_name}' already exists. It will be overwritten.")
        
        map_obj.save(file_name)
        print(f"Map has been saved to '{file_name}'.")

    except ValueError as e:
        print(f"Validation Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Main function to run the program
def main() -> None:
    """
    Main function to get user input for start and end locations and create a map with predefined waypoints.
    """
    try:
        start = validate_input(input("Enter the start location (address or place name): "))
        end = validate_input(input("Enter the end location (address or place name): "))
        
        create_map(start, end)
        print("Map creation completed!")
    
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
