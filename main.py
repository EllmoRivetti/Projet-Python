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

DATA = dict()
DepInReg = dict()
DicPop = dict()
      

def set_up():
    Departement.set_up()
    Gare.set_up()
    Perte.set_up()
    Region.set_up()
    instantiateDict()

def instantiateDict():
    #Fill the DicPop Dictionnary
    f = open("pop.txt","r",encoding="utf-8")
    for line in f.readlines():
        splt = line.split(":")
        DicPop[splt[0]] = (int) (splt[1].split("\n")[0])

    print("DicPop: ")
    print(DicPop)

    #Fill the DepInReg Dictionnary
    for reg in Region.DATA:
        for dep in Departement.DATA:
            if reg.code == dep.regionCode:
                if not reg.name in DepInReg:
                    DepInReg[reg.name] = list()
                DepInReg[reg.name].append(dep.name)
    
    #Fill the DicNbObjPerYear Dictionnary
    for obj in Perte.DATA:
        date = obj.date.split(" ")[2]
        if not date in DicNbObjPerYear:
            DicNbObjPerYear[date] = 1
        DicNbObjPerYear[date] += 1


def clean_up():
    for url_and_file_list in list(FICHIERS.values()):
        file = url_and_file_list["file_name"] 
        try:
            os.remove(file)
        except:
            pass

def getGareByUIC(uic):
    pass

def isDepartementInRegion(departement,region):
    if not (region in DepInReg):
        print("This region doesn't exist")
    
    return departement in DepInReg[region]

def getRegionForDepartement(departement):
    for key in DepInReg.keys():
        if isDepartementInRegion(departement,key):
            return key
    print("This departement doesn't exist")

def main():
    print("\n--------\n")
    print("Nombre de gares: ", len(LISTE_GARES))
    print("Informations des gares: ", Gare._meta.key_aliases)
    print("Exemple: ", Gare.DATA[0])

    print("\n--------\n")
    print("Nombre de pertes: ", len(PERTES))
    print("Informations des pertes: ", Perte._meta.key_aliases)
    print("Exemple: ", Perte.DATA[0])

    print("\n--------\n")
    print("Nombre de departements: ", len(LISTE_DEPARTEMENTS))
    print("Informations des departements: ", Departement._meta.key_aliases)
    print("Exemple: ", Departement.DATA[0])

    print("\n--------\n")
    print("Nombre de regions: ", len(LISTE_REGIONS))
    print("Informations des regions: ", Region._meta.key_aliases)
    print("Exemple: ", Region.DATA[0])

if __name__ == '__main__':
    clean    = False
    for arg in sys.argv:
        if arg in ["-c", "-clean"]:
            clean = True

    set_up()
    main()
    if clean:
        clean_up()