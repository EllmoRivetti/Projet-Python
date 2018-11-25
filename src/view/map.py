import folium
import os
import json
import pandas as pd
from src.tools import Tools

geojson = {
    'region': 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson',
    'departement': 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson' 
}
class Map():
    pass
    @staticmethod 
    def draw(pertes, annee):
        headers = ['Departement', 'Pertes en ' + str(annee)]
        data = dict()
        for region in pertes.keys():
            for dep in pertes[region].keys():
                data[dep] = pertes[region][dep][annee]
        s = pd.Series(data, name='Pertes en ' + str(annee))
        s.index.name = 'Departement'
        s.reset_index()
        data = s
        print(data)
        print('\n\n')

        m = folium.Map(location=[48.862, 2.346], zoom_start=3)
        m.choropleth(
            geo_data=geojson['departement'],
            name='choropleth',
            key_on='feature.properties.school_dist',
            columns=headers,
            data=data,
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2
        )
        m.save('results_'+str(annee)+'.html')
