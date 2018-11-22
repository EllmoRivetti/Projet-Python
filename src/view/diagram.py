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
        
        print("List nb: "+listeNb)
        print("List years: "+listeBins)

        plt.hist(listeNb, bin=listeBins)

        n, bins, patches = plt.hist(x, bins=b)

        plt.xlabel('Années')
        plt.ylabel('Somme des objets perdus')
        plt.title("Nombre d'objet perdus dans les gares SNCF de 2014 à 2018")

        plt.show()
        #TODO APPEL DANS LE MAIN