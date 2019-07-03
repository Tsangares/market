from Saveable import Saveable
from db import marketdb
_commodity=marketdb.commodity

class Commodity(Saveable):
    def __init__(self,name):
        self.name=name
        self.save()
    def data():
        return {'name': self.name }
    def save(self):
        super(Commodity,self).save(_commodity)
        
