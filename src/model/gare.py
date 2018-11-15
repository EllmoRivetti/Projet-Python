from donnee import Donnee

class Gare():
    DATA = list()
    _meta = Donnee(
        url             = "https://data.sncf.com/explore/dataset/liste-des-gares/download/?format=json&timezone=Europe/Berlin",
        file_name       = "liste-des-gares.json",
        keys            = ["departement", "commune", "code_uic", "coordonnees_geographiques", "libelle_gare"], 
        key_aliases     = ["departement", "commune", "uic", "coordonnees", "label"], 
        critical_keys   = ["coordonnees_geographiques",], 
        size            = "5MB",
        compressed      = False
    )

    def __init__(self, _date, _type, _uic):
        self.date = _date
        self.type = _type
        self.uic  = _uic
        Pertes.DATA.append(self)