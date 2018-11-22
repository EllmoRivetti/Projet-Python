import folium
import os
 

class Map():
    # def __init__(self, departements, gares, pertes):
    #     pertesParDepartement = dict() # keys -> departements; value -> count des pertes

    #     for perte in pertes:
    #         gare = getGareByUIC(perte['uic'])
    #         departement = DATA['x']
    
    # def draw(self, ):
    pass
    @staticmethod 
    def draw():
        shapefile = os.path.abspath(os.path.join('data', 'departements-20180101'))
        m = folium.Map(location=[48.864716, 2.349014])
        m

    # @staticmethod
    # def display(myMap):
    #     from IPython.display import HTML, display
    #     LDN_COORDINATES = (51.5074, 0.1278) 
    #     myMap._build_map()
    #     mapWidth, mapHeight = (400,500) # width and height of the displayed iFrame, in pixels
    #     srcdoc = myMap.HTML.replace('"', '&quot;')
    #     embed = HTML('<iframe srcdoc="{}" '
    #                 'style="width: {}px; height: {}px; display:block; width: 50%; margin: 0 auto; '
    #                 'border: none"></iframe>'.format(srcdoc, width, height))
    #     embed