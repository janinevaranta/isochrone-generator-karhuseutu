# Generates overpass way-nodes into a line. Returns GeoDataFrame.

from shapely import geometry
from shapely.ops import linemerge, unary_union
from geopandas import GeoSeries

from app.fetch_data import fetch_overpass_data

def fetch_satakunta_borders():
    satakunta_query = """
    [out:json];
    rel[name=Satakunta]["ISO3166-2"="FI-17"];
    out geom;
    """
    satakunta_data = fetch_overpass_data(satakunta_query)["elements"][0]["members"][1:]
    return satakunta_data

def generate_ways_to_line():
    way_list = []

    data = fetch_satakunta_borders()

    for way in data:
        coords = []
        for node in way["geometry"]:
            coords.append((node["lon"],node["lat"]))
        way_list.append(geometry.LineString(coords))

    merged = linemerge([*way_list])
    borders = list(unary_union(merged))
    gpd_series = GeoSeries(borders,crs="epsg:4326")
    return gpd_series