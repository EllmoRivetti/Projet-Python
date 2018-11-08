import numpy as np
import matplotlib.pyplot as plt

FICHIERS = {
    "LISTE_GARES" : {
        "url"               : "https://data.sncf.com/explore/dataset/liste-des-gares/download/?format=json&timezone=Europe/Berlin",
        "file_name"         : "liste-des-gares.json", 
        "data_keys"         : ["departement", "commune", "code_uic", "coordonnees_geographiques", "libelle_gare"],
        "data_keys_aliases" : ["departement", "commune", "uic", "coordonnees", "label"],
        "critical_keys"     : ["coordonnees_geographiques",],
    }, 
    "PERTES"      : {
        "url"               : "https://data.sncf.com/explore/dataset/objets-trouves-gares/download/?format=json&timezone=Europe/Berlin", 
        "file_name"         : "pertes.json",
        "data_keys"         : ["date", "gc_obo_nom_recordtype_sc_c", "gc_obo_gare_origine_r_code_uic_c",],
        "data_keys_aliases" : ["date", "type", "uic",],
        "critical_keys"     : ["gc_obo_gare_origine_r_code_uic_c",],
    },
    "LISTE_DEPARTEMENTS" : {
        "url"               : "https://www.data.gouv.fr/fr/datasets/r/5c219016-1eaf-41dc-9bba-2f32dfb71b72",
        "file_name"         : "French-zip-code-3.0.0-JSON/json/departements.json",
        "data_keys"         : ["region_code","name"],
        "data_keys_aliases" : ["region_code","DepName"],
        "critical_keys"     : ["region_code","name"],
    },
    "LISTE_REGIONS" : {
         "url"               : "https://www.data.gouv.fr/fr/datasets/r/5c219016-1eaf-41dc-9bba-2f32dfb71b72",
        "file_name"         : "French-zip-code-3.0.0-JSON/json/regions.json",
        "data_keys"         : ["code","name"],
        "data_keys_aliases" : ["codeReg","RegName"],
        "critical_keys"     : ["code","name"],
    },
}

DATA = dict()


def download_file(url, filename):
    import urllib.request
    response = urllib.request.urlopen(url)
    html = response.read()
    binfile = open(filename, "wb")
    binfile.write(html)
    binfile.close()

def set_up(download=True):
    for CURRENT_DATA_NAME in FICHIERS.keys():
        DATA[CURRENT_DATA_NAME] = list()
        if download:
            import urllib.request
            urllib.request.urlretrieve(FICHIERS[CURRENT_DATA_NAME]["url"], FICHIERS[CURRENT_DATA_NAME]["file_name"])
        import json

        with open(FICHIERS[CURRENT_DATA_NAME]["file_name"]) as f:
            RAW_FILE_JSON = json.loads(''.join(f.readlines()))
            for line in RAW_FILE_JSON:
                l = dict()
                all_critical_keys_in_entry = True
                for critical_key in FICHIERS[CURRENT_DATA_NAME]["critical_keys"]:
                    if not critical_key in line['fields'].keys():
                        all_critical_keys_in_entry = False
                if all_critical_keys_in_entry:
                    for key, value in line['fields'].items():
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

def clean_up():
    import os
    for url_and_file_list in list(FICHIERS.values()):
        file = url_and_file_list["file_name"] 
        try:
            os.remove(file)
        except:
            pass

def showDiagrams():
    pass


def main():
    LISTE_GARES = DATA["LISTE_GARES"]
    PERTES = DATA["PERTES"]

    print("\n--------\n")
    print("Nombre de gares: ", len(LISTE_GARES))
    print("Informations des gares: ", list(LISTE_GARES[0].keys()))
    print("Exemple: ", LISTE_GARES[0])

    print("\n--------\n")
    print("Nombre de pertes: ", len(PERTES))
    print("Informations des pertes: ", list(PERTES[0].keys()))
    print("Exemple: ", PERTES[0])
    showDiagrams()


if __name__ == '__main__':
    import sys
    download = False
    clean    = False
    for arg in sys.argv:
        if arg in ["-d", "-download"]:
            download = True
        if arg in ["-c", "-clean"]:
            clean = True

    set_up(download=download)
    main()
    if clean:
        clean_up()