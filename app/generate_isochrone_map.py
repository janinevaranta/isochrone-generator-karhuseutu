# The main function to generate the end product.
# TODO: Translate the Finnish comments into English.
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def isochrone_generator(isoc_area, borders, point_locations, base_map, isoc_colors=[], point_color="grey", center_name="", buffer_zone=0, buffer_interval=0, buffer_color="black", map_color="grey", background_color="white", line_color="white"):
    # Isokroni-tiedoston GeoDataFrame. Muuten Suomen viralliseen projektiomuotoon.
    isoc_area = isoc_area.to_crs(epsg=2393) 
    # Luodaan alueelle raja.
    covered_area = isoc_area.geometry.unary_union 
    area_borders = borders.to_crs(epsg=2393)
    # Poistetaan kaikki kohteet rajojen ulkopuolella.
    point_locations = point_locations.to_crs(epsg=2393) 
    point_locations = point_locations[point_locations.geometry.within(covered_area)]
    
    # Base vetoaa pohjakarttaan. Kartta piirretään ja sitä voi käyttää sen jälkeen pohjana muille elementeille.
    base = base_map.to_crs(epsg=2393).plot(color=map_color, figsize=(10,7), edgecolor=line_color, linewidth=0.1)
    base.set_facecolor(background_color)
    area_borders.plot(ax=base, edgecolor="black", linestyle="--")
    # Piirretään isokroni-alue ja karttaan tulevat kohteet.
    isoc_area.plot(ax=base, color=isoc_colors)
    point_locations.plot(ax=base, color=point_color, edgecolor="black", linewidth=1.0)

    # Lisätään kartan pisteisiin otsikot ja talletetaan kartan keskipiste.
    center_x = 0
    center_y = 0
    for x, y, label in zip(point_locations.geometry.x,point_locations.geometry.y,point_locations.name):
        base.annotate(label, size=12, xy=(x,y), xytext=(-6,6), textcoords="offset points")
        center_x = x
        center_y = y

    # Rajataan karttanäkymä. Oletuksena näyttäisi kaiken, mitä ollaan piirretty, mutta koko Suomi on turhan iso alue.
    xmin,ymin,xmax,ymax = isoc_area.loc[3]["geometry"].bounds
    mod = 15000 # Yksikkönä metrit.

    plt.xlim((xmin-mod,xmax+mod)) # Kartalle piirretyn isokronin mitat + mod.
    plt.ylim((ymin-mod,ymax+mod))

    # Piirretään buffer ympyrät. Yksikkönä toimii metrit.
    buffer = buffer_zone # Metreissä.
    for c in range(1,1+buffer_interval):
        circle = plt.Circle((center_x,center_y), radius=buffer*c, color=buffer_color, fill=False)
        base.add_artist(circle) # Circle-olio täytyy lisätä erikseen artistina karttaan. Katso matplotlibin ohjeet.

    # Tehdään kartalle kuvaustekstit.
    patch15 = mpatches.Patch(color=isoc_colors[3], label="15 min")
    patch30 = mpatches.Patch(color=isoc_colors[2], label="30 min")
    patch45 = mpatches.Patch(color=isoc_colors[1], label="45 min")
    patch60 = mpatches.Patch(color=isoc_colors[0], label="60 min")

    plt.legend(handles=[patch15,patch30,patch45,patch60])

    plt.show()