import folium
import os

import json
import pandas as pd
import numpy as np

import src  
from src.tools import Tools

geojson = {
    'region': 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson',
    'departement': 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson' 
}
class Map():
    
    @staticmethod
    def parseData(pertes, annee):
        file_path = os.path.join('data','departement.geojson')
        Tools.download_file(geojson['departement'], file_path)
        RAW_FILE_GEOJSON = None
        with open(file_path, 'r') as f:
            RAW_FILE_GEOJSON = json.loads(''.join(f.readlines()))
        for i in range(len(RAW_FILE_GEOJSON['features'])):
            RAW_FILE_GEOJSON['features'][i]['id'] = RAW_FILE_GEOJSON['features'][i]['properties']['code']

        headers = ['Departement', 'Pertes en ' + str(annee)]
        departementByCode = dict()
        for departement in src.model.departement.Departement.DATA:
            departementByCode[departement.name] = departement.code
        data = dict()
        for region in pertes.keys():
            for dep in pertes[region].keys():
                if dep in departementByCode:
                    departementCode = departementByCode[dep]
                    if (len(str(departementCode)) == 1):
                        departementCode = '0' + str(departementCode)
                    data[str(departementCode)] = pertes[region][dep][annee]
        return headers, data, RAW_FILE_GEOJSON

    @staticmethod 
    def draw(pertes, annee):
        headers, data, RAW_FILE_GEOJSON = Map.parseData(pertes, annee)
        quantiles = list()
        for i in [0, 0.25, 0.5, 0.75, 1]:
            quantiles.append(np.quantile(list(data.values()), i))        
        quantiles = [0, 50, 100, 250, 500, 1000]   
        data = pd.Series(data, name='Pertes en ' + str(annee))
        data.index.name = 'Departement'
        data.reset_index()
        # print(data.to_string())
        # print(headers)
        # print(quantiles)
        # print(RAW_FILE_GEOJSON['features'][0]['properties'])
        # print(data[RAW_FILE_GEOJSON['features'][0]['id']])

        m = folium.Map(location=[47.081, 2.3987], zoom_start=6)
        m.choropleth(
            geo_data=RAW_FILE_GEOJSON,
            name='Pertes par département en ' + str(annee),
            key_on='feature.id',
            columns=headers,
            data=data,
            legend_name='Pertes par Departement (par unité)',
            fill_color='YlGn',
            threshold_scale=quantiles,
            fill_opacity=0.7,
            line_opacity=0.2,
        )
        folium.LayerControl().add_to(m)
        m.save('results_'+str(annee)+'.html')