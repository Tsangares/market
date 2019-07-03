#Script used for building the environment.
from pymongo import MongoClient
from Market import Market
from Business import Business #cluster0-7aeh1.azure.mongodb.net
client=MongoClient('mongodb+srv://sailor:O9d4*eBJkizk@cluster0-7aeh1.azure.mongodb.net/test?retryWrites=true&w=majority')
marketdb=client.market_test
business=marketdb.business
market=marketdb.market
canvas=marketdb.canvas
transactions=marketdb.canvas_transactions

def setPoint(x,y,r,g,b):
    color={
        'x': x,
        'y': y,
        'r': r,
        'g': g,
        'b': b,
    }
    return canvas.update_one({'x': x, 'y': y}, {'$set': color},upsert=True)
    
for i in range(100):
    for j in range(100):
        print(i,j,setPoint(i,j,10,10,10))
        
        
'''
sc=Market("Santa Cruz", (5,0))
nike=Business("Nike",sc,100,10)
adidas=Business("Adidas",sc,77,33)
sc.save()
'''
'''
sc=Market('Santa Cruz',(1,3))
sf=Market('San Francisco',(-2,7))
rwc=Market('Redwood City',(10,-8))


#nike=Business('Nike',sc,300,30)
#adidas=Business('Adidas',sf,200,20)
asic=Business('Asic',sf,200,20)
reebok=Business('Reebok',sf,200,20)
sketchers=Business('Sketchers',rwc,200,20)
puma=Business('Puma',rwc,200,20)
vans=Business('Vans',sf,200,20)
sf.save()
rwc.save()
'''

test=Market.load("Santa Cruz")
print(test,test.businesses)
