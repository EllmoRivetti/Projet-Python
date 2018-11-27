import folium
import os
import json
import pandas as pd
from src.tools import Tools
import src

geojson = {
    'region': 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson',
    'departement': 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson' 
}
class Map():
    pass
    @staticmethod 
    def draw(pertes, annee):
        file_path = os.path.join('data','departement.json')
        Tools.download_file(geojson['departement'], file_path)
        RAW_FILE_GEOJSON = None
        with open(file_path, 'r') as f:
            RAW_FILE_GEOJSON = json.loads(''.join(f.readlines()))
        for i in range(len(RAW_FILE_GEOJSON['features'])):
            RAW_FILE_GEOJSON['features'][i]['id'] = RAW_FILE_GEOJSON['features'][i]['properties']['code']

        headers = ['Departement', 'Pertes en ' + str(annee)]
        data = dict()
        for region in pertes.keys():
            for dep in pertes[region].keys():
                departement = src.model.departement.Departement.getDepartementByName(dep)
                if departement:
                    print(departement.code)
                    data[departement.code] = pertes[region][dep][annee]
        s = pd.Series(data, name='Pertes en ' + str(annee))
        s.index.name = 'Departement'
        s.reset_index()
        data = s
        print(data)
        print('\n\n')
        # bins = list(state_data['Unemployment'].quantile([0, 0.25, 0.5, 0.75, 1]))

        m = folium.Map(location=[48.862, 2.346], zoom_start=3)
        m.choropleth(
            geo_data=RAW_FILE_GEOJSON,
            name='choropleth',
            key_on='feature.properties.school_dist',
            columns=headers,
            data=data,
            legend_name='Pertes par Departement (%)',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            reset=True
        )
        m.save('results_'+str(annee)+'.html')
