from math import sqrt
from db import marketdb
from Saveable import Saveable
_market=marketdb.market
class Market(Saveable):
    def __init__(self,name,position=(0,0)):
        super(Market,self).__init__()
        self.name=name
        self.businesses=[]
        self.position=position
        self._id=Saveable.getId(name,_market)

    def load(d):
        from Business import Business
        d=Saveable.load(d,_market)
        market=Market(d['name'],d['position'])
        market._id=d['_id']
        for business in d['businesses']:
            Business.load(business,market)
        return market
    
    def save(self):
        for b in self.businesses: b.save()
        super(Market,self).save(_market)

    def data(self):
        return {
            'name': self.name,
            'businesses': [b._id for b in self.businesses],
            'position': self.position,
        }
    def __repr__(self):
        return self.name
    
    def display(self):
        for business in self.businesses:
            business.display()

    def getDistance(self,market):
        x=market.position[0]-self.position[0]
        y=market.position[1]-self.position[1]
        return sqrt(x**2 + y**2)
    
    def addBusiness(self,business):
        self.businesses.append(business)




