from Market import Market
from Business import Business
import random
import time
sc=Market('Santa Cruz',(1,3))
sf=Market('San Francisco',(-2,7))
rwc=Market('Redwood City',(10,-8))


nike=Business('Nike',sc,300,30)
adidas=Business('Adidas',sf,200,20)
asic=Business('Asic',sf,200,20)
reebok=Business('Reebok',sf,200,20)
sketchers=Business('Sketchers',rwc,200,20)
puma=Business('Puma',rwc,200,20)
vans=Business('Vans',sc,200,20)

sketchers.setAskPrice(1)
sketchers.setBidPrice(30)

print("All the businesses are setup.\n")
time.sleep(4)
rwc.display()

time.sleep(4)
print("Sending out convoys\n")
convoy=puma.createConvoy(cost=70,money=30,quantity=5)
convoy.setAskPrice(1)
convoy.gotoMarket(sc,[(vans,2),(nike,3)])
time.sleep(4)
convoy2=vans.createConvoy(cost=10,money=5,quantity=1)
convoy2.gotoMarket(sf,[(asic,1),(reebok,1)])
time.sleep(4)
print("\nAttempting to make a trasaction with a convoy while they are traveling.")
convoy.sell(nike,3)

time.sleep(4)
rwc.display()

time.sleep(4)
print("\nDelaying for 15 secconds. While convoys travel.")
time.sleep(15)

print("\nAttempting to make a convoy transact.")
convoy.sell(nike,3)

time.sleep(4)
print("\nDelaying for 20 secconds. While convoys travel home.")
time.sleep(10)

rwc.display()



