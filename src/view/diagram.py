import numpy as np
import collections
import matplotlib.pyplot as plt

class Diagram:
    #Afficher un histogramme representant le nombre de pertes par années. abscisse: année / ordonnée: nb perte
    def __init__(self,perteByGare):
        self.perteByGare = perteByGare

    def drawDiagram(self):
        listeBins = [1,100,200,300,400,500,600,700,800,900,1000]
        listValue = list()

        for elem in self.perteByGare.keys():
            listValue.append(self.perteByGare[elem])

        plt.hist(listValue ,bins= listeBins,edgecolor = 'black')

        plt.xlabel("Nombre d'objets perdus")
        plt.ylabel("Nombre de gares")
        plt.title("Représentation du nombre de gares (ayant au moins une perte) selon un intervalle de quantité d'objets perdus.")

        plt.show()