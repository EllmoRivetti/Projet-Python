from donnee import Donnee

class Perte():
    DATA = list()
    _meta = Donnee(
        url             = "https://data.sncf.com/explore/dataset/objets-trouves-gares/download/?format=json&timezone=Europe/Berlin", 
        #si vous telechargez ce fichier manuellement veuillez le renommer en "pertes.json"
        file_name       = "pertes.json",
        keys            = ["date", "gc_obo_nom_recordtype_sc_c", "gc_obo_gare_origine_r_code_uic_c",], 
        key_aliases     = ["date", "type", "uic",], 
        critical_keys   = ["gc_obo_gare_origine_r_code_uic_c",], 
        size            = "330MB",
        compressed      = False
    )

    def __init__(self, _date, _type, _uic):
        self.date = _date
        self.type = _type
        self.uic  = _uic
        Pertes.DATA.append(self)