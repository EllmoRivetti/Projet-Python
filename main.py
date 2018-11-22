# Extern libraries
import json
import os
import os.path
import folium
import sys

# Intern libraries
from src.model.donnee import Donnee
from src.model.departement import Departement
from src.model.gare import Gare
from src.model.perte import Perte
from src.model.region import Region

from src.tools import Tools

from src.view.diagram import Diagram
from src.view.map import Map

DEBUG = False
DicPop = dict()
ListNbObjLostPerYear = list()
      

def set_up():

    Departement.set_up()
    Gare.set_up()
    Perte.set_up()
    Region.set_up()
    instantiateCollections()
    diagram = Diagram(ListNbObjLostPerYear)
    diagram.drawDiagram()

def instantiateCollections():
    #Fill the DicPop Dictionnary
    f = open("pop.txt","r",encoding="utf-8")
    for line in f.readlines():
        splt = line.split(":")
        DicPop[splt[0]] = (int) (splt[1].split("\n")[0])

    print("DicPop: ")
    print(DicPop)

    #Fill the Departement.DepInReg Dictionnary
    for reg in Region.DATA:
        for dep in Departement.DATA:
            if reg.code == dep.region_code:
                if not reg.name in Departement.DepInReg:
                    Departement.DepInReg[reg.name] = list()
                Departement.DepInReg[reg.name].append(dep.name)
    
    #Fill the DicNbObjPerYear Dictionnary
    for obj in Perte.DATA:
        date = obj.date[0:4]
        ListNbObjLostPerYear.append(int(date))


def clean_up():
    folder = Donnee.DATA_FOLDER
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def getGareByUIC(uic):
    pass

def main():
    if DEBUG:
        print("\n--------\n")
        print("Nombre de gares: ", len(Gare.DATA))
        print("Informations des gares: ", Gare._meta.key_aliases)
        print("Exemple: " + str(Gare.DATA[0]))

        print("\n--------\n")
        print("Nombre de pertes: ", len(Perte.DATA))
        print("Informations des pertes: ", Perte._meta.key_aliases)
        print("Exemple: ", Perte.DATA[0])

        print("\n--------\n")
        print("Nombre de departements: ", len(Departement.DATA))
        print("Informations des departements: ", Departement._meta.key_aliases)
        print("Exemple: ", Departement.DATA[0])

        print("\n--------\n")
        print("Nombre de regions: ", len(Region.DATA))
        print("Informations des regions: ", Region._meta.key_aliases)
        print("Exemple: ", Region.DATA[0])

if __name__ == '__main__':
    clean    = False
    for arg in sys.argv:
        if arg in ["--c", "--clean"]:
            clean = True

    if clean:
        clean_up()
        print("Succesfully deleted data folder !")
    else:
        print("Launching Program")
        set_up()
        main()
    