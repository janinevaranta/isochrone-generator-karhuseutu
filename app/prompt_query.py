# Prompts the user for a query specific questions.

def prompt_query(town_df):
    coordinates = []
    # Ask the user for the place from where the isochrone will originate.
    def get_location_coordinates_on_map(location_name):   
        # Check if the given location exists as a name on the fetched database.
        if location_name in town_df["name"].values:
            print("Kohde löytyi!")
            # The series has to be changed into a numpy array.
            # This is because otherwise, the body cannot be constructed in json format
            # because of all the extra stuff that comes when you extract a value from pandas cell.
            s = town_df.loc[town_df["name"]==location_name].to_numpy()
            lon = s[0][2]
            lat = s[0][1]
            return [lon,lat]
        else:
            print("Kohdetta ei löytynyt.")
            return False

    name = input("Anna kaupungin tai kunnan nimi: ")
    loc = get_location_coordinates_on_map(name.capitalize())
    if loc != False:
        lon, lat = loc
    else:
        lon = input("Anna leveysaste: ")
        lat = input("Anna pituusaste: ")
        name = ""

    coordinates.append(lon)
    coordinates.append(lat)

    return (coordinates, name)

