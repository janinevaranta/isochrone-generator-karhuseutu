# Generate the fetched isochrone data into a polygon and return them as GeoDataFrame.
import json
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Polygon

def generate_isochrone_polygons(data):
    iso_df = pd.json_normalize(json.loads(data), "features")

    # Remove the extra dimension from the arrays.
    iso_df["geometry.coordinates"].loc[0] = iso_df["geometry.coordinates"].loc[0][0]
    iso_df["geometry.coordinates"].loc[1] = iso_df["geometry.coordinates"].loc[1][0]
    iso_df["geometry.coordinates"].loc[2] = iso_df["geometry.coordinates"].loc[2][0]
    iso_df["geometry.coordinates"].loc[3] = iso_df["geometry.coordinates"].loc[3][0]
    
    # Transform the coordinates into polygon objects.
    iso_df["geometry"] = iso_df["geometry.coordinates"].apply(Polygon)
    
    # Cleanup the dataframe by dropping extra columns.
    iso_df.drop(["geometry.coordinates", "geometry.type"], axis=1, inplace=True)

    # Transform pandas dataframe into geodataframe.
    iso_df = GeoDataFrame(iso_df, geometry="geometry", crs="epsg:4326").sort_values(by="properties.value",ascending=False)

    return iso_df