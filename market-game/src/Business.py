from Trader import Trader
from Convoy import Convoy
from Saveable import Saveable
import Market
from db import marketdb
_business=marketdb.business

class Business(Trader,Saveable):
    def __init__(self,name,market,money=0,quantity=0,ask=20,bid=10):
        super(Business,self).__init__(name,market,money,quantity,ask,bid)
        market.addBusiness(self)
        self.convoys=[]
        
        
    def load(d,market=None):
        d=Saveable.load(d,_business)
        if d is None:
            print("This business does not exist! Check spelling; it is case sensitive!")
            return None
        if market is None:
            market=Market.Market.load(d['market'])
        return Business(d['name'],market,d['money'],d['quantity'],d['askPrice'],d['bidPrice'])
    
    def save(self):
        super(Business,self).save(_business)

    def display(self):
        print("The business %s:"%self)
        print("\tMoney = $%.02f"%self.money)
        print("\tQuantity =  %d"%self.quantity)
        print("\tAsking Price = $%.02f"%self.askPrice)
        print("\tBiding Price = $%.02f"%self.bidPrice)
        print("\tConvoys: ",self.convoys)
        print("\n")

        
        
    def data(self):
        data=super(Business,self).data()
        data['convoys']=len(self.convoys)
        data['market']=self.market._id
        return data
    
    def createConvoy(self,cost,money=0,quantity=0):
        convoy=Convoy(self,cost,money,quantity)
        self.money-=money+cost
        self.quantity-=quantity
        self.convoys.append(convoy)
        return convoy

