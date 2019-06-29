class Business:
    def __init__(self,name):
        self.name=name
        self.money=100
        self.quantity=100 #Number of units/shoes
        self.askPrice=20 #Price they are willing to sell at
        self.bidPrice=10 #Price they are willing to buy at

    def __repr__(self):
        return self.name

    def setBidPrice(self,price):
        self.bidPrice=price
        
    def setAskPrice(self,price):
        self.askPrice=price
    

    #Assume a transaction from A to B
    def transact(A,B,units,buy=True,sell=True):
        buyPrice=(A.bidPrice-B.askPrice)/2 + B.askPrice
        sellPrice=(B.bidPrice-A.askPrice)/2 + A.askPrice
        if buy and A.bidPrice >= B.askPrice:
            #Sucessful purchase
            A.quantity+=units
            A.money-=buyPrice*units
            B.quantity-=units
            B.money+=buyPrice*units
            print("Purchase succeeded between %s to %s at $%.02f with %s units"%(A.name,B.name,buyPrice,units))
            return True
        elif sell and B.bidPrice >= A.askPrice:
            #Sucessful sale
            A.quantity-=units
            A.money+=sellPrice*units
            B.quantity+=units
            B.money-=sellPrice*units
            print("Sale succeeded between %s to %s at $%.02f with %s units"%(A.name,B.name,sellPrice,units))
            return True
        else:
            #Failed transaction.
            print("Transaction failed between %s and %s."%(A.name,B.name))
            return False
    
    #self is buying from business
    def buy(self,business,units):
        return Business.transact(self,business,units,sell=False)

    #business is buying from self
    def sell(self,business,units):
        return Business.transact(self,business,units,buy=False)
