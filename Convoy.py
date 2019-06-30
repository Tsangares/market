from Trader import Trader
from numpy.random import normal
from threading import Timer
import time
from Trader import Trader
class Convoy(Trader):
    def __init__(self,owner,cost,money=0,quantity=0,ask=20,bid=10):
        name="%s's Convoy #%d"%(owner.name,len(owner.convoys))
        super(Convoy,self).__init__(name,owner.market)
        self.cost=cost
        self.quantity=quantity
        self.speed=self.getSpeed(cost)
        self.destination=None
        self.origin=owner.market
        self.owner=owner
        self.businesses=[]
        print("Convoy created, ",self)
        
    def getSpeed(self,money):
        slowest=.5
        fastest=2
        scale=money/300
        if scale > 1: scale=1
        loc=slowest + (fastest-slowest) * scale
        spread=slowest*(1-scale)
        speed = normal(loc,spread)
        if speed > fastest: return fastest
        if speed < slowest: return slowest
        return speed

    def getTransitTime(self,market):
        return self.market.getDistance(market)/self.speed
    
    def gotoMarket(self,destination,businesses):
        if len(businesses) < 1:
            print("Must have specify which businesses to transact with.")
            return
        self.businesses=businesses
        self.setMarket(destination,self.arrivedRemote)


    #businesses is a tuple array (busisness,quantity)
    def setMarket(self,destination,finished):
        transitTime=self.getTransitTime(destination)
        print("%s going to %s will take %.02f sec."%(self,destination,transitTime))
        self.destination=destination
        self.market=None
        timer=Timer(transitTime,finished)
        timer.start()

    def goHome(self):
        self.setMarket(self.origin,self.arrivedHome)
        
    def arrivedRemote(self):
        print(self,"arrived.")
        self.market=self.destination
        self.destination=None
        for business,quantity in self.businesses:
            Trader.transact(self,business,quantity)
            time.sleep(2)
        self.goHome()
        
    def arrivedHome(self):
        if self.destination is not self.origin:
            raise Exception("Error wrong market")
        self.market=self.destination
        self.destination=None
        self.owner.money += self.money
        self.money=0
        self.owner.quantity += self.quantity
        self.quantity=0
        print(self.owner.convoys)
        del self.owner.convoys[self.owner.convoys.index(self)]
        print(self.owner.convoys)

