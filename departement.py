from src.donnee import Donnee

class Departement(Donnee):

    DATA = list()

    def __init__(self,regionCode,name):
        self.regionCode = regionCode
        self.name = name

        Departement.DATA.append(self)

