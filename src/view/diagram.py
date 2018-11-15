import numpy as np
import matplotlib.pyplot as plt

class Diagram:
    #Afficher un histogramme representant le nombre de pertes par années. abscisse: année / ordonnée: nb perte
    def __init__(self,nbLostObjPerYears):
        self.nbLostObjPerYears = nbLostObjPerYears

    def drawDiagram(self):
        listeNb = list()
        listeBins = set()
        for year in self.nbLostObjPerYears.keys():
            list.append(self.nbLostObjPerYears[year])
            listeBins.add(year)
        
        plt.hist(listeNb, bin=listeBins)

        #TODO APPEL DANS LE MAIN