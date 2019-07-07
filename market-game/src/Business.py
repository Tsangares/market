from Trader import Trader
from Convoy import Convoy
from Saveable import Saveable
from Commodity import Stock
import Market
from db import marketdb
_business=marketdb.business

class Business(Trader,Saveable):
    def __init__(self,name,market,money=0,stock=None):
        super(Business,self).__init__(name,market,money,stock)
        market.addBusiness(self)
        self.convoys=[]
        
    def load(d,market=None):
        d=Saveable.load(d,_business)
        if d is None:
            print("This business does not exist! Check spelling; it is case sensitive!")
            return None
        if market is None:
            market=Market.Market.load(d['market'],deep=False)
        print("Getting %s's stock info..."%d['name'])
        stock={name: Stock.load(s) for name,s in d['stock'].items()}
        return Business(d['name'],market,d['money'],stock)
    def save(self):
        super(Business,self).save(_business)

    def display(self,commodity=None):
        print("|===== {:^11.10} =====|".format(self.name))
        print("|  Money      ${:<8.2f} |".format(self.money))
        print("|-------  Stock  -------|")
        print("|                       |")
        stocks=self.stock.items()
        if commodity is not None:
            stocks=[(commodity,self.stock[commodity])]
        for name,stock in stocks:
            print("|****   {:^9.6}   ****|".format(name))
            print("| Quantity:    {:<8d} |".format(stock.quantity))
            if stock.buyPrice > 1000:
                print("| Buy Price:  ${:06.2e} |".format(stock.buyPrice))
            else:
                print("| Buy Price:  ${:<8.2f} |".format(stock.buyPrice))
            if stock.sellPrice > 1000:
                print("| Sell Price: ${:06.2e} |".format(stock.sellPrice))
            else:
                print("| Sell Price: ${:<8.2f} |".format(stock.sellPrice))
            print("|                       |")
        print("|=======================|\n")
        
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

