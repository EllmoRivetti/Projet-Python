import urllib.request
import json
import os
import sys
import os.path
import zipfile

FICHIERS = {
    "LISTE_GARES" : {
        "url"                       : "https://data.sncf.com/explore/dataset/liste-des-gares/download/?format=json&timezone=Europe/Berlin",
        "file_name"                 : "liste-des-gares.json", 
        "data_keys"                 : ["departement", "commune", "code_uic", "coordonnees_geographiques", "libelle_gare"],
        "data_keys_aliases"         : ["departement", "commune", "uic", "coordonnees", "label"],
        "critical_keys"             : ["coordonnees_geographiques",],
        "approximative_file_size"   : "5MB",
          "compressed_file"			: False,
    }, 
    "PERTES"      : {
        "url"                       : "https://data.sncf.com/explore/dataset/objets-trouves-gares/download/?format=json&timezone=Europe/Berlin", 
        "file_name"                 : "pertes.json",
        "data_keys"                 : ["date", "gc_obo_nom_recordtype_sc_c", "gc_obo_gare_origine_r_code_uic_c",],
        "data_keys_aliases"         : ["date", "type", "uic",],
        "critical_keys"             : ["gc_obo_gare_origine_r_code_uic_c",],
        "approximative_file_size"   : "330MB",
          "compressed_file"			: False,
    }, 
    "LISTE_DEPARTEMENTS" : {
        "url"               		: "https://www.data.gouv.fr/fr/datasets/r/5c219016-1eaf-41dc-9bba-2f32dfb71b72",
        "file_name"         		: "departments.json",
        "data_keys"         		: ["region_code","name"],
        "data_keys_aliases" 		: ["region_code","DepName"],
        "critical_keys"     		: ["region_code","name"],
        "approximative_file_size"   : "9Ko",
        "compressed_file"			: {"name": "French-zip-code-3.0.0-JSON.zip", "path":["json"]},
    },
    "LISTE_REGIONS" : {
        "url"               		: "https://www.data.gouv.fr/fr/datasets/r/5c219016-1eaf-41dc-9bba-2f32dfb71b72",
        "file_name"         		: "regions.json",
        "data_keys"         		: ["code","name"],
        "data_keys_aliases" 		: ["codeReg","RegName"],
        "critical_keys"     		: ["code","name"],
        "approximative_file_size"   : "2Ko",
        "compressed_file"			: {"name": "French-zip-code-3.0.0-JSON.zip", "path":["json"]},
    },
}

DATA = dict()
DepInReg = dict()
DicPop = dict()

def progress_bar(blocks_transfered, block_size, total_size):
    import sys
    size = 20
    done_percentage = (blocks_transfered * block_size/total_size) * 100
    sys.stdout.flush()
    sys.stdout.write("[")
    for i in range(size):
        if i < done_percentage/100*size:
            sys.stdout.write("-")
        else:
            sys.stdout.write(" ")
    sys.stdout.write("] - ")
    sys.stdout.write(str(done_percentage).split('.')[0])
    sys.stdout.write("%")

    # print(blocks_transfered * block_size)
    # print(block_size)
    # print(total_size)
    os.system("cls") 

def download_file(CURRENT_DATA_NAME):
    # response = urllib.request.urlopen(url)
    # html = response.read()
    # binfile = open(filename, "wb")
    # binfile.write(html)
    # binfile.close()
    if not FICHIERS[CURRENT_DATA_NAME]["compressed_file"]:
        urllib.request.urlretrieve(FICHIERS[CURRENT_DATA_NAME]["url"], FICHIERS[CURRENT_DATA_NAME]["file_name"], progress_bar)
    else:
        urllib.request.urlretrieve(FICHIERS[CURRENT_DATA_NAME]["url"], FICHIERS[CURRENT_DATA_NAME]["compressed_file"]["name"], progress_bar)

def open_file(CURRENT_DATA_NAME):
    try:
        return open(FICHIERS[CURRENT_DATA_NAME]["file_name"])
    except:
        archive = zipfile.ZipFile(FICHIERS[CURRENT_DATA_NAME]["compressed_file"]["name"], 'r')
        path = []
        path.extend(FICHIERS[CURRENT_DATA_NAME]["compressed_file"]["path"])
        path.append(FICHIERS[CURRENT_DATA_NAME]["file_name"])
        print(path)
        path_to_file = os.path.join(*path)
        path_to_file = path_to_file.replace('\\', '/')

        print(archive.namelist())
        file = archive.open(path_to_file)
        with open(FICHIERS[CURRENT_DATA_NAME]["file_name"], 'wb+') as f:
            for line in file.readlines():
                f.write(line)
        

def read_json_data_from_file(f, CURRENT_DATA_NAME):
    RAW_FILE_JSON = json.loads(''.join(f.readlines()))
    for raw_line in RAW_FILE_JSON:
        line = raw_line
        if 'fields' in raw_line:
            line = raw_line['fields']

        l = dict()
        all_critical_keys_in_entry = True
        for critical_key in FICHIERS[CURRENT_DATA_NAME]["critical_keys"]:
            if not critical_key in line.keys():
                all_critical_keys_in_entry = False

        if all_critical_keys_in_entry:
            for key, value in line.items():
                if key in FICHIERS[CURRENT_DATA_NAME]["data_keys"]:
                    index_key = FICHIERS[CURRENT_DATA_NAME]["data_keys"].index(key)
                    alias = FICHIERS[CURRENT_DATA_NAME]["data_keys_aliases"][index_key]
                    try:
                        l[alias] = int(value)
                    except ValueError:
                        l[alias] = value
                    except TypeError:
                        l[alias] = value 
            DATA[CURRENT_DATA_NAME].append(l)

def set_up(download=True):
    for CURRENT_DATA_NAME in FICHIERS.keys():
        DATA[CURRENT_DATA_NAME] = list()
        if download and not os.path.isfile(FICHIERS[package]["file_name"]):
            download_file(CURRENT_DATA_NAME)

        f = open_file(CURRENT_DATA_NAME)
        try:
            print(f, CURRENT_DATA_NAME)
            read_json_data_from_file(f, CURRENT_DATA_NAME)
        except:
            # print("The data file ", FICHIERS[CURRENT_DATA_NAME]["file_name"], " seem to be corrupted. Re-run the script with the download parameter.")
            print("You don't have the data file ", FICHIERS[CURRENT_DATA_NAME]["file_name"], " or this file is corrupted. Do you agree to download this file (Approximative size: ", FICHIERS[CURRENT_DATA_NAME]["approximative_file_size"], " ? (yes/no)")
            download = (str(input()).lower() == "yes")
            if not download:
                print("Exiting..")
                exit()
            else:
                download_file(CURRENT_DATA_NAME)
                f = open(FICHIERS[CURRENT_DATA_NAME]["file_name"])
                read_json_data_from_file(f, CURRENT_DATA_NAME)
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