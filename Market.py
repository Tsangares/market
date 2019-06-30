from math import sqrt
class Market:
    def __init__(self,name,position=(0,0)):
        self.name=name
        self.businesses=[]
        self.position=position

    def __repr__(self):
        return self.name
    
    def display(self):
        for business in self.businesses:
            print("The business %s:"%business)
            print("\tMoney: $%.02f"%business.money)
            print("\tQuantity: %d"%business.quantity)
            print("\tAsk,Bid: %.02f,%.02f"%(business.askPrice,business.bidPrice))
            print("\tConvoys: ",business.convoys)
            print("\n")

    def getDistance(self,market):
        x=market.position[0]-self.position[0]
        y=market.position[1]-self.position[1]
        return sqrt(x**2 + y**2)
    
    def addBusiness(self,business):
        self.businesses.append(business)




