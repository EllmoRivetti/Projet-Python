from src.model.donnee import Donnee

class Departement():

    DATA = list()
    _meta = None

    @staticmethod
    def set_up():
        _meta = Donnee(
            url             = "https://www.data.gouv.fr/fr/datasets/r/5c219016-1eaf-41dc-9bba-2f32dfb71b72",
            file_name       = "departments.json",
            keys            = ["region_code","name"],
            key_aliases     = ["region_code","DepName"],
            critical_keys   = ["region_code","name"],
            size            = "9Ko",
            archive_name    = "French-zip-code-3.0.0-JSON.zip",
            archive_path    = ["json"],
            parent_class    = 'departement'
        )

    def __init__(self):
        Departement.DATA.append(self)

