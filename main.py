#!python3 - Isochrone-Generator

#***************************************************************************************************************
# A tool to generate isochrone maps in Finland, in Finnish.
# This tool is a part of exploration of different Business Intelligence
# tools and methods to promote development of rural tourism destinations.
# This specific tools explores and promotes the usage of public APIs for tourism destinations
# to visualize their destination's accessibility.
#***************************************************************************************************************
# Created by Jani Nevaranta, 2022, Project Researcher at Satakunta University of Applied Sciences (SAMK)
# for Tiedolla johtaminen matkailun menestystekijäksi Karhuseudun alueella -project.
# Project funded by LEADER Karhuseutu, The European Agricultural Fund for Rural Development.
#***************************************************************************************************************

# TODO: Install Folium and use it as the base map.

import warnings

import geopandas as gpd

from shapely.errors import ShapelyDeprecationWarning

from app.prompt_query import prompt_query
from app.fetch_data import fetch_isochrone_data
from app.generate_town_locations import generate_town_locations
from app.generate_isochrone_polygons import generate_isochrone_polygons
from app.generate_ways_to_line import generate_ways_to_line
from app.generate_isochrone_map import isochrone_generator

# TODO: Temporary fix. Mainly affects Shapely.
# Update code later to conform to the warnings.
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

# Stop pandas false positive warnings.
import pandas as pd
pd.options.mode.chained_assignment = None

def main():
    print("Ladataan Suomen kartta...")
    finland_df = gpd.read_file("data/kuntarajat2022.geojson")
    print("Ladataan Suomen kaupungit kartalle...")
    town_df = generate_town_locations()
    print("Luodaan maakunnan rajat")
    borders_df = generate_ways_to_line()

    center_coordinates, center_name, method = prompt_query(town_df) 

    print("API-kutsu tehty OpenRouteServiceen. Odotetaan vastausta...")
    iso_data = fetch_isochrone_data(center_coordinates, method, api_key_file_path=r"keys/api_key_ors.txt")
    print("Luodaan isokroni-alueet...")
    iso_df = generate_isochrone_polygons(iso_data)

    print("Luodaan kartta...")
    isochrone_generator(
        iso_df,
        borders_df, 
        town_df, 
        finland_df, 
        ["lightseagreen","turquoise","paleturquoise","white"], 
        "ivory", 
        center_name, 
        10000,
        5, 
        "ivory", 
        map_color="lightslategrey",
        background_color="lightcyan"
    )
    print("Valmis!")    


if __name__ == "__main__":
    main()
