# Generates the locations of the towns and cities in Finland into dataframe.

import json
from pandas import DataFrame
from geopandas import GeoDataFrame, points_from_xy

from app.fetch_data import fetch_overpass_data

def overpass_transform_marker_nodes_to_df(data):
    # Returns geojson data of towns as pandas dataframe.
    nodes = []
    for i, node in enumerate(data["elements"]):
        obj = {}
        try:
            obj["name"] = node["tags"]["name"]
        except:
            obj["name"] = ""
        try:
            obj["lat"] = node["lat"]
            obj["lon"] = node["lon"]
        except:
            obj["lat"] = 0
            obj["lon"] = 0
        nodes.append(obj)
    df = DataFrame(nodes)
    return df

def generate_town_locations():
    # Returns GeoDataFrame object of the town locations fetched from overpass query.

    # Check if the data already exists. If not, generate one from OpenStreetMap.
    #TODO: Implement pathlib module and transfer data to "/data" location.
    town_file = "towns.txt"
    try:
        with open(town_file, "r") as f:
            raw_data = f.read()
            towns_data = json.loads(raw_data)
            print("Ladattu tiedostosta!")
    except:
        town_query = """[out:json];
            area[admin_level=2]["ISO3166-1"=FI]->.a;
            (
            node[place=town](area.a)(60.253441567136015,20.0115966796875,62.48695302124994,26.0430908203125);
            node[place=city](area.a)(60.253441567136015,20.0115966796875,62.48695302124994,26.0430908203125);
            );
            out;
        """
        towns_data = fetch_overpass_data(town_query)
        # Save the fetched data to avoid repeating.
        with open(town_file, "w") as f:
            json.dump(towns_data, f, ensure_ascii=False)
        print("Ladattu Overpass APIsta ja tallennettu tiedostoksi /data/towns.txt")


    df = overpass_transform_marker_nodes_to_df(towns_data)
    town_locs = GeoDataFrame(df, geometry=points_from_xy(df.lon,df.lat), crs="epsg:4326")

    return town_locs