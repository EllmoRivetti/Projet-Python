import folium
import os

geojson = {
    'region': 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson',
    'departement': 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson' 
}
class Map():
    pass
    @staticmethod 
    def draw():
        shapefile = os.path.abspath(os.path.join('data', 'departements-20180101'))
        center = [48.862, 2.346]
        paris = folium.Map(center, zoom_start=13)
        folium.Marker(center, popup='Les Halles').add_to(paris)
        paris.save('results.html')
