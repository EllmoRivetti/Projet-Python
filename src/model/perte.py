from src.model.donnee import Donnee

class Perte():
    DATA = list()
    _meta = None
    tries = dict()
    
    @staticmethod
    def set_up():
        Perte._meta = Donnee(
            url             = "https://data.sncf.com/explore/dataset/objets-trouves-gares/download/?format=json&timezone=Europe/Berlin", 
            #si vous telechargez ce fichier manuellement veuillez le renommer en "pertes.json"
            file_name       = "pertes.json",
            keys            = ["date", "gc_obo_nom_recordtype_sc_c", "gc_obo_gare_origine_r_code_uic_c",], 
            key_aliases     = ["date", "type", "uic",], 
            critical_keys   = ["gc_obo_gare_origine_r_code_uic_c",], 
            size            = "330MB",
            parent_class    = "perte"
        )

    def __init__(self):
        self.date = None
        self.type = None
        self.uic = None
        Perte.DATA.append(self)

    def __str__(self):
        return "Perte: [ date: " + str(self.date) + ", type: " + str(self.type) + ", uic: " + str(self.uic) + " ]"
