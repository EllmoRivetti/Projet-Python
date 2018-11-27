# Extern libraries
from subprocess import call
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
Annees = [2014, 2015, 2016, 2017, 2018]
DicPop = dict()
ListNbObjLostPerYear = list()

def set_up():
    Departement.set_up()
    Gare.set_up()
    Perte.set_up()
    Region.set_up()
    instantiateCollections()
    
    Map.draw(Perte.tries, 2018)
    diagram = Diagram(ListNbObjLostPerYear)
    diagram.drawDiagram()
    

def instantiateCollections():
    #Fill the DicPop Dictionnary
    f = open("pop.txt","r",encoding="utf-8")
    for line in f.readlines():
        splt = line.split(":")
        DicPop[splt[0]] = (int) (splt[1].split("\n")[0])
        
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

    # PertesParRegion/Departement
    departements_inconnus = list()
    pertes_ignores = 0

        # instantiating all data
    for region in Region.DATA:
        Perte.tries[region.name] = dict()
        
        for departement in Departement.DATA:
            if Departement.isDepartementInRegion(departement.name, region.name):
                Perte.tries[region.name][departement.name] = dict()
                for annee in Annees:
                    Perte.tries[region.name][departement.name][annee] = 0

        Perte.tries[region.name]['all'] = dict()
        for annee in Annees:
            Perte.tries[region.name]['all'][annee] = 0

    gareByUic = dict()
    for gare in Gare.DATA:
        gareByUic[gare.uic] = gare
    #more efficient than a getGareByUic since we don't loop over gares for all pertes.

    i = 0
    for perte in Perte.DATA:
        i += 1
        Tools.global_progress_bar("Computing losses by regions and departements... ", i, len(Perte.DATA))
        for annee in Annees:
            if str(perte.date[0:4]) == str(annee):
                if perte.uic in gareByUic:
                    gare =  gareByUic[perte.uic]
                    if gare:
                        departement = Departement.getDepartementByName(gare.departement)
                        if departement:
                            region = Departement.getRegionForDepartement(departement.name) 
                            Perte.tries[region.name]['all'][annee] += 1
                            Perte.tries[region.name][departement.name][annee] += 1
                        else:
                            if not gare.departement in departements_inconnus:
                                departements_inconnus.append(gare.departement)
                    else:
                        pertes_ignores += 1
    
    if pertes_ignores > 0:
        print('Failed to retrieve information from', pertes_ignores, 'pertes ! (there are', len(Perte.DATA), ' pertes)')
    else:
        print('All the pertes have been treated.')
    if len(departements_inconnus) > 0:
        print('There are ', len(departements_inconnus), ' unknown departements !')
        print(departements_inconnus) 
    if DEBUG:
        print('\n##############')
        print(Perte.tries)




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

def set_up_environment():
    with open("requirements.txt") as f:
        for line in f.readlines():
            call(['pip', 'install', line])
            os.system('cls')

def set_up_end_environment():
    with open("requirements.txt") as f:
        for line in f.readlines():
            call(['pip', 'install', str(line).split('==')[0]])


if __name__ == '__main__':
    os.system('cls')
    set_up_environment()
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
    set_up_end_environment()
