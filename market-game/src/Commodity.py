from Saveable import Saveable
from db import marketdb
from sys import maxsize
_commodity=marketdb.commodity
class Stock:
    def __init__(self,commodity,quantity=0,buyPrice=1,sellPrice=1e3):
        self.name=commodity.name
        self.commodity=commodity
        self.buyPrice=buyPrice
        self.sellPrice=sellPrice
        self.quantity=quantity

    def load(data):
        return Stock(Commodity.load(data['name']),data['quantity'],data['buy'],data['sell'])
    def data(self):
        return {
            'name': self.name,
            'buy': self.buyPrice,
            'sell': self.sellPrice,
            'quantity': self.quantity,
        }
        
class Commodity(Saveable):
    def __init__(self,name,_id=None):
        self.name=name
        self.save()
        self._id=_id
    def __repr__(self):
        return "Commodity %s"%self.name
    def load(name):
        data=Saveable.load(name,_commodity)
        return Commodity(data['name'],data['_id'])
    def data(self):
        return {'name': self.name }
    def save(self):
        super(Commodity,self).save(_commodity)
    def all():
        collect=[]
        cursor=_commodity.find({})
        for commodity in cursor:
            collect.append(Commodity(commodity['name']))
        return collect
    def getStock(self):
        return Stock(self)
        
