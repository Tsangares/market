from Commodity import Commodity,Stock

class Trader:
    def __init__(self,name,market,money=0,stock=None):
        super(Trader,self).__init__()
        self.name=name
        self.market=market
        self.money=money
        if stock is None:
            stock={c.name: c.getStock() for c in Commodity.all()}
        elif issubclass(type(stock),list) and len([s for s in stock if issubclass(type(s),Stock)])>0:
            stock={c.name: c for c in stock}
        elif not issubclass(type(stock),dict):
            raise Exception("The stock should be a dictionary.",stock)
        self.stock=stock

    def data(self):
        return {
            'name': self.name,
            'money': self.money,
            'stock': {stock.name: stock.data() for key,stock in self.stock.items()}
        }
    
    def setMarket(self,market):
        self.market=market
        
    def __repr__(self):
        return "%s (%s)"%(self.name,self.market)

    def setBuyPrice(self,commodity,price):
        if issubclass(type(commodity),Commodity):
            commodity=commodity.name
        self.stock['commodity'].buyPrice=price
        
    def setSellPrice(self,commodity,price):
        if issubclass(type(commodity),Commodity):
            commodity=commodity.name
        self.stock['commodity'].buyPrice=price

    def spend(self,money):
        if self.money-money < 0:
            print("Cannot transact! Not enough money.")
            return False
        else:
            self.money-=money
            return True

    #Assume a transaction from A to B
    def transact(A,B,commodity,units,buy=None,sell=None):
        if units <= 0:
            print("Wrong parameters in transaction.")
            return None
        if not issubclass(Commodity,type(commodity)):
            raise Exception("Old transaction occured! Please update to support commodities.")
        if A.market is None or B.market is None or A.market.name != B.market.name:
            print("Wrong market; no sale.",A,B)
            return None

        print("#---- %s ----#---- %s ----#---- %s ----#"%(A.name,commodity,B.name))
        stockA=A.stock[commodity.name]
        stockB=B.stock[commodity.name]

        buyPrice=(stockA.buyPrice-stockB.sellPrice)/2 + stockB.sellPrice
        sellPrice=(stockB.buyPrice-stockA.sellPrice)/2 + stockA.sellPrice

        #Check if they are willing and if they have the quantity to sell
        #TODO: TEST: If I want 5 but they only have 4, buy the 4.
        canBuy=stockA.buyPrice >= stockB.sellPrice and stockB.quantity>0
        canSell=stockB.buyPrice >= stockA.sellPrice and stockA.quantity>0

        buyEnabled= buy is None or buy is True
        sellEnabled= sell is None or sell is True

        isOnlySell= sell is True and buy is None
        isOnlyBuy = buy is True and sell is None
                    
        if canBuy and buyEnabled and not isOnlySell:
            if stockB.quantity-units<0:
                return Trader.transact(A,B,commodity,stockB.quantity,buy,sell)
            if A.spend(buyPrice*units):
                stockA.quantity+=units
                stockB.quantity-=units
                B.money+=buyPrice*units
                print("Purchase succeeded between %s to %s at $%.02f with %s %s pigments."%(A.name,B.name,buyPrice,units,commodity.name))
                return True
            else:
                print("Purchase failed, because %s does not have enough money."%A)
        elif canSell and sellEnabled and not isOnlyBuy:
            if stockA.quantity-units<0:
                return Trader.transact(A,B,commodity,stockA.quantity,buy,sell)
            if B.spend(sellPrice*units):
                stockA.quantity-=units
                A.money+=sellPrice*units
                stockB.quantity+=units
                print("Sale succeeded between %s to %s at $%.02f with %s %s pigments."%(A.name,B.name,sellPrice,units,commodity.name))
                return True
            else:
                print("Sale failed, because %s does not have enough money."%B)
        else:
            #Failed transaction.
            print("No transaction could be made between %s and %s.\n Try lowering your sell price or raising your buy price."%(A,B))
            return False
    
    #self is buying from business
    def buy(self,business,commodity,units):
        return Trader.transact(self,business,commodity,units,buy=True)

    #business is buying from self
    def sell(self,business,commodity,units):
        return Trader.transact(self,business,commodity,units,sell=True)

if __name__=='__main__':
    from Market import Market
    cod=Commodity('cod')
    tuna=Commodity('tuna')
    mall=Market('test',exports=[cod,tuna])
    joe=Trader('joe',mall,money=100,stock=[Stock(cod,10,15,10),Stock(tuna,0,10,15)])
    ken=Trader('ken',mall,money=100,stock=[Stock(cod,0,10,15),Stock(tuna,10,15,10)])
    joe.sell(ken,cod,20)

    
