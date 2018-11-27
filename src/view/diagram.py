import numpy as np
import collections
import matplotlib.pyplot as plt

class Diagram:
    #Afficher un histogramme representant le nombre de pertes par années. abscisse: année / ordonnée: nb perte
    def __init__(self,nbLostObjPerYears):
        self.nbLostObjPerYears = nbLostObjPerYears

    def drawDiagram(self):
        listeBins = list()
        #for elem in nbLostObjPerYears:

        # print("Map nb lost: ", self.nbLostObjPerYears)
        for elem in self.nbLostObjPerYears:
            if not elem == 2013: # les données de 2013 étant entrée vers la fin d'année, par conséquent elles ne sont pas cohérentes
                if not elem in listeBins:
                    listeBins.append(elem)
        listeBins.sort();
        listeBins.append(max(listeBins)+1)
        #listeBins=[2013,2014,2015,2016,2017,2018,2019]

        # count13 = 0
        # count14 = 0
        # count15 = 0
        # count16 = 0
        # count17 = 0
        # count18 = 0

        # for elem in self.nbLostObjPerYears:
        #     if elem == 2013:
        #         count13+=1
        #     elif elem == 2014:
        #         count14+=1
        #     elif elem == 2015:
        #         count15+=1
        #     elif elem == 2016:
        #         count16+=1
        #     elif elem == 2017:
        #         count17+=1
        #     elif elem == 2018:
        #         count18+=1

        # print("2013: ",count13)
        # print("2014: ",count14)
        # print("2015: ",count15)
        # print("2016: ",count16)
        # print("2017: ",count17)
        # print("2018: ",count18)

        #print("List nb: ", self.nbLostObjPerYears)
        print("List years: ", listeBins)

        plt.hist(self.nbLostObjPerYears ,bins= listeBins,
            edgecolor = 'black')

        plt.xlabel('Années')
        plt.ylabel("Total d'objets perdus")
        plt.title("Nombre d'objet perdus dans les gares SNCF de "+str(min(listeBins))+" à aujourd'hui")#+str(max(listeBins)))

        plt.show()
        #TODO APPEL DANS LE MAIN