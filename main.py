import geopandas as gpd

from app.prompt_query import prompt_query
from app.fetch_data import fetch_isochrone_data
from app.generate_town_locations import generate_town_locations
from app.generate_isochrone_polygons import generate_isochrone_polygons
from app.generate_ways_to_line import generate_ways_to_line
from app.generate_isochrone_map import isochrone_generator

def main():
    print("Ladataan Suomen kartta...")
    finland_df = gpd.read_file("/Volumes/OuterMemory/Downloads/kuntarajat.geojson")
    print("Ladataan Suomen kaupungit kartalle...")
    town_df = generate_town_locations()
    print("Luodaan maakunnan rajat")
    borders_df = generate_ways_to_line()

    center_coordinates, center_name = prompt_query(town_df) 

    print("API-kutsu tehty OpenRouteServiceen. Odotetaan vastausta...")
    iso_data = fetch_isochrone_data(center_coordinates, api_key_file_path=r"/Volumes/OuterMemory/SAMK/api_key_ors.txt")
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
