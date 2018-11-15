from src.donnee import Donnee

class Region(Donnee):

    DATA = list()

    def __init__(self,regionCode,name):
        self.regionCode = regionCode
        self.name = name

        Region.DATA.append(self)

