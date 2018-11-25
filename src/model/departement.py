import src 
class Departement():

    DATA = list()
    DepInReg = dict()
    _meta = None

    @staticmethod
    def set_up():
        Departement._meta = src.model.donnee.Donnee(
            url             = "https://www.data.gouv.fr/fr/datasets/r/5c219016-1eaf-41dc-9bba-2f32dfb71b72",
            file_name       = "departments.json",
            keys            = ["region_code","name"],
            key_aliases     = ["region_code","name"],
            critical_keys   = ["region_code","name"],
            size            = "9Ko",
            archive_name    = "French-zip-code-3.0.0-JSON.zip",
            archive_path    = ["json"],
            parent_class    = 'departement'
        )

    def __init__(self):
        self.name = None
        self.region_code = None
        src.model.departement.Departement.DATA.append(self)

    def __str__(self):
        return "Departement: [ Nom: " + str(self.name) + ", region_code: " + str(self.region_code) + " ]"

    @staticmethod
    def isDepartementInRegion(departement,region):
        if not (region in Departement.DepInReg):
            print("This region doesn't exist")
            print(departement)
            print(region)
        for entry in Departement.DepInReg[region]:
            if src.tools.Tools.strip_accents(entry) == src.tools.Tools.strip_accents(departement):
                return True
        return False

    @staticmethod
    def getRegionForDepartement(departement):
        for key in Departement.DepInReg.keys():
            if Departement.isDepartementInRegion(departement,key):
                return src.model.region.Region.getRegionByName(key)
        return None

    @staticmethod
    def getDepartementByName(name):
        for entry in Departement.DATA:
            if name == entry.name:
                return entry
        return None
