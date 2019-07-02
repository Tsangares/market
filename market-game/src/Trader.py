class Trader:
    def __init__(self,name,market,money=0,quantity=0,ask=20,bid=10):
        super(Trader,self).__init__()
        self.name=name
        self.market=market
        self.money=money
        self.quantity=quantity #Number of units/shoes
        self.askPrice=ask #Price they are willing to sell at
        self.bidPrice=bid #Price they are willing to buy at

    def data(self):
        return {
            'name': self.name,
            #'type': str(type(self)),
            'money': self.money,
            'quantity': self.quantity,
            'askPrice': self.askPrice,
            'bidPrice': self.bidPrice,
            }
    
    def setMarket(self,market):
        self.market=market
        
    def __repr__(self):
        return "%s (%s)"%(self.name,self.market)

    def setBidPrice(self,price):
        self.bidPrice=price
        
    def setAskPrice(self,price):
        self.askPrice=price
    
    def spend(self,money):
        if self.money-money < 0:
            print("Cannot transact! Not enough money.")
            return False
        else:
            self.money-=money
            return True

    #Assume a transaction from A to B
    def transact(A,B,units,buy=None,sell=None):
        if A.market is None or B.market is None or A.market.name != B.market.name:
            print("Wrong market; no sale.",A,B)
            return None
        buyPrice=(A.bidPrice-B.askPrice)/2 + B.askPrice
        sellPrice=(B.bidPrice-A.askPrice)/2 + A.askPrice
        isOnlySell= sell is True and buy is None
        isOnlyBuy = buy is True and sell is None
        if (buy is None or buy is True) and not isOnlySell and A.bidPrice >= B.askPrice:
            #Sucessful purchase
            A.quantity+=units
            A.spend(buyPrice*units)
            B.quantity-=units
            B.money+=buyPrice*units
            print("Purchase succeeded between %s to %s at $%.02f with %s units"%(A.name,B.name,buyPrice,units))
            return True
        elif (sell is None or sell is True) and not isOnlyBuy and B.bidPrice >= A.askPrice:
            #Sucessful sale
            A.quantity-=units
            A.money+=sellPrice*units
            B.quantity+=units
            B.spend(sellPrice*units)
            print("Sale succeeded between %s to %s at $%.02f with %s units"%(A.name,B.name,sellPrice,units))
            return True
        else:
            #Failed transaction.
            print("Transaction failed between %s and %s."%(A.name,B.name))
            return False
    
    #self is buying from business
    def buy(self,business,units):
        return Trader.transact(self,business,units,sell=False)

    #business is buying from self
    def sell(self,business,units):
        return Trader.transact(self,business,units,buy=False)
