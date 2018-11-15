import json
import os
import os.path
import folium

DATA = dict()
DepInReg = dict()
DicPop = dict()
      

def set_up(download=True):
    
    instantiateDict()

def instantiateDict():
    #Fill the DicPop Dict
    f = open("pop.txt","r",encoding="utf-8")
    for line in f.readlines():
        splt = line.split(":")
        DicPop[splt[0]] = (int) (splt[1].split("\n")[0])

    print("DicPop: ")
    print(DicPop)

    #Fill the DepInReg Dict
    

    

def clean_up():
    for url_and_file_list in list(FICHIERS.values()):
        file = url_and_file_list["file_name"] 
        try:
            os.remove(file)
        except:
            pass

def drawDiagrams():
    #TODO Créer un dict pour stocker une list de departement pour chaque région. ex : {"Ile-de-France":["Paris","Yvelines",...]}
    #TODO Créer un dict pour stocker la population pour chaque région. ex : {"Ile-de-France":12000000,...}
    pass

def getGareByUIC(uic):
    pass
class Map():
    def __init__(self, departements, gares, pertes):
        pertesParDepartement = dict() # keys -> departements; value -> count des pertes

        for perte in pertes:
            gare = getGareByUIC(perte['uic'])
            departement = DATA['x']
    
    def draw(self, ):
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
    LISTE_GARES = DATA["LISTE_GARES"]
    PERTES = DATA["PERTES"]
    LISTE_DEPARTEMENTS = DATA["LISTE_DEPARTEMENTS"]
    LISTE_REGIONS = DATA["LISTE_REGIONS"]



    print("\n--------\n")
    print("Nombre de gares: ", len(LISTE_GARES))
    print("Informations des gares: ", list(LISTE_GARES[0].keys()))
    print("Exemple: ", LISTE_GARES[0])

    print("\n--------\n")
    print("Nombre de pertes: ", len(PERTES))
    print("Informations des pertes: ", list(PERTES[0].keys()))
    print("Exemple: ", PERTES[0])

    print("\n--------\n")
    print("Nombre de departements: ", len(LISTE_DEPARTEMENTS))
    print("Informations des departements: ", list(LISTE_DEPARTEMENTS[0].keys()))
    print("Exemple: ", LISTE_DEPARTEMENTS[0])

    print("\n--------\n")
    print("Nombre de regions: ", len(LISTE_REGIONS))
    print("Informations des regions: ", list(LISTE_REGIONS[0].keys()))
    print("Exemple: ", LISTE_REGIONS[0])

if __name__ == '__main__':
    download = False
    clean    = False
    for arg in sys.argv:
        if arg in ["-d", "-download"]:
            download = True
        if arg in ["-c", "-clean"]:
            clean = True

    dataFilesNotOnDisk = True
    for package in FICHIERS.keys():
        if not os.path.isfile(FICHIERS[package]["file_name"]):
            dataFilesNotOnDisk = False
            print(str(FICHIERS[package]["file_name"]) + " not found on disk.")
    if not dataFilesNotOnDisk:
        print("You don't have all the data files. You need the data files in order for the program to work correctly. Do you agree to download them ? (yes/no)")
        download = (str(input()).lower() == "yes")
        if not download:
            print("Exiting..")
            exit()


    set_up(download=download)
    main()
    if clean:
        clean_up()