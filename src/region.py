from donnee import Donnee

class Region:

    DATA = list()
    _meta = Donnee(
        url = "https://www.data.gouv.fr/fr/datasets/r/5c219016-1eaf-41dc-9bba-2f32dfb71b72",
        file_name = "regions.json",
        keys = ["code","name"],
        key_aliases = ["code","name"],
        critical_keys = ["code","name"],
        size = "2Ko",
        archive_name = "French-zip-code-3.0.0-JSON.zip",
        archive_path = ["json"]
    )

    def __init__(self,regionCode,name):
        self.regionCode = regionCode
        self.name = name

        Region.DATA.append(self)

