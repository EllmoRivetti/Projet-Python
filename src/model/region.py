from src.model.donnee import Donnee

class Region:
    DATA = list()
    _meta = None

    @staticmethod
    def set_up():
        Region._meta = Donnee(
            url             = "https://www.data.gouv.fr/fr/datasets/r/5c219016-1eaf-41dc-9bba-2f32dfb71b72",
            file_name       = "regions.json",
            keys            = ["code","name"],
            key_aliases     = ["code","name"],
            critical_keys   = ["code","name"],
            size            = "2Ko",
            archive_name    = "French-zip-code-3.0.0-JSON.zip",
            archive_path    = ["json"],
            parent_class    = "region"
        )

    def __init__(self):
        self.name = None
        self.code = None
        Region.DATA.append(self)

    def __str__(self):
        return "Perte: [ name: " + str(self.name) + ", code: " + str(self.code) + " ]"

    @staticmethod
    def getRegionByName(name):
        for entry in Region.DATA:
            if name == entry.name:
                return entry
        return None