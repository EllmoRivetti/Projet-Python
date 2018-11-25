from src.model.donnee import Donnee


class Gare():
    DATA = list()
    _meta = None

    @staticmethod
    def set_up():
        Gare._meta = Donnee(
            url             = "https://data.sncf.com/explore/dataset/liste-des-gares/download/?format=json&timezone=Europe/Berlin",
            file_name       = "liste-des-gares.json",
            keys            = ["departement", "commune", "code_uic", "coordonnees_geographiques", "libelle_gare"], 
            key_aliases     = ["departement", "commune", "uic", "coordonnees", "label"], 
            critical_keys   = ["coordonnees_geographiques",], 
            size            = "5MB",
            parent_class    = "gare"
        )

    def __init__(self):
        self.departement = None
        self.commune = None
        self.uic = None
        self.coordonnees = None
        self.label = None
        Gare.DATA.append(self)

    def __str__(self):
        return "Gare: [ departement: " + str(self.departement) + ", commune: " + str(self.commune) + ", uic: " + str(self.uic) + ", coordonnees: " + str(self.coordonnees) + ", label: " + str(self.label) + " ]"

    @staticmethod
    def getGareByUIC(uic):
        for entry in Gare.DATA:
            if entry.uic == uic:
                return entry
        return None