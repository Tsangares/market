from Trader import Trader
from Convoy import Convoy

class Business(Trader):
    def __init__(self,name,market,money=0,quantity=0,ask=20,bid=10):
        super(Business,self).__init__(name,market,money,quantity,ask,bid)
        market.addBusiness(self)
        self.convoys=[]

    def createConvoy(self,cost,money=0,quantity=0):
        convoy=Convoy(self,cost,money,quantity)
        self.money-=money+cost
        self.quantity-=quantity
        self.convoys.append(convoy)
        return convoy

