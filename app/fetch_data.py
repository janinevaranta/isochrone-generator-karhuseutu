# Helper functions to generate overpass and OpenRouteService queries and 
# fetch data from them.
import requests

def fetch_overpass_data(query=""):
    # Fetch OpenStreetMap data from Overpass API.
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = query
    response = requests.get(overpass_url, params={"data":overpass_query})
    print(response.status_code, response.reason)
    data = response.json()
    return data

def fetch_isochrone_data(coordinates=[], method=1, area_range=3600, interval=900, api_key_file_path=""):
    # Fetch isochrone data from OpenRouteService API.
    # Requires API key from the service. Limited calls.
    body = {"locations":[coordinates],"range":[area_range],"interval":interval}
    api_key = ""

    methods_dict = {
        "1": "driving-car",
        "2": "cycling-regular",
        "3": "foot-walking"
    }

    chosen_method = methods_dict[str(method)]

    with open(api_key_file_path, "r") as f:
        api_key = f.read()
        
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': api_key,
        'Content-Type': 'application/geo+json; charset=utf-8'
    }
    response = requests.post(f"https://api.openrouteservice.org/v2/isochrones/{chosen_method}", json=body, headers=headers)
    print(response.status_code, response.reason)

    data = response.text
    return data
        

    