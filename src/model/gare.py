from src.model.donnee import Donnee

class Gare():
    DATA = list()
    _meta = None

    @staticmethod
    def set_up():
        _meta = Donnee(
            url             = "https://data.sncf.com/explore/dataset/liste-des-gares/download/?format=json&timezone=Europe/Berlin",
            file_name       = "liste-des-gares.json",
            keys            = ["departement", "commune", "code_uic", "coordonnees_geographiques", "libelle_gare"], 
            key_aliases     = ["departement", "commune", "uic", "coordonnees", "label"], 
            critical_keys   = ["coordonnees_geographiques",], 
            size            = "5MB",
            compressed      = False,
            parent_class    = "gare"
        )

    def __init__(self):
        Pertes.DATA.append(self)