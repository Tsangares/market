from Market import Market
from Business import Business
import random
myMarket=Market('valeria')
myBiz=Business('Nike')
urBiz=Business('Addidas')

myMarket.addBusiness(myBiz)
myMarket.addBusiness(urBiz)

print( "My market is named %s" % myMarket.name )
print( "%s containes the businesses: %s\n" % (myMarket.name, myMarket.businesses) )

while not myBiz.sell(urBiz, 5):
    print("My ask price $%.02f"%myBiz.askPrice, " ur bid price $%.02f"%urBiz.bidPrice)
    myBiz.setAskPrice(myBiz.askPrice-random.random())
    urBiz.setBidPrice(urBiz.bidPrice+random.random())

for business in myMarket.businesses:
    print("The business %s:"%business)
    print("\tMoney: $%.02f"%business.money)
    print("\tQuantity: %d"%business.quantity)
    print("\n")

