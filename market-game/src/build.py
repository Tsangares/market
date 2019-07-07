#Script used for building the environment.
from pymongo import MongoClient
from Market import Market
from Commodity import Commodity
from Business import Business #cluster0-7aeh1.azure.mongodb.net
client=MongoClient('mongodb+srv://sailor:O9d4*eBJkizk@cluster0-7aeh1.azure.mongodb.net/test?retryWrites=true&w=majority')
marketdb=client.market_test
business=marketdb.business
market=marketdb.market
canvas=marketdb.canvas
transactions=marketdb.canvas_transactions

def buildCommodities():
    from Commodity import Commodity
    red=Commodity('red')
    blue=Commodity('blue')
    green=Commodity('green')
    red.save()
    blue.save()
    green.save()

def buildMarkets():
    red=Commodity.load('red')
    green=Commodity.load('green')
    blue=Commodity.load('blue')
    
    sc=Market("Santa Cruz", (5,0), exports=[red])
    sf=Market('San Francisco',(-2,7),exports=[green])
    rwc=Market('Redwood City',(10,-8),exports=[blue])

    nike=Business("Nike",sc,100)
    adidas=Business("Adidas",sc,77)
    asic=Business('Asic',sf,200)
    reebok=Business('Reebok',sf,200)
    sketchers=Business('Sketchers',rwc,200)
    puma=Business('Puma',rwc,200)
    vans=Business('Vans',sf,200)

    nike.stock['Red'].quantity+=1
    nike.stock['Blue'].quantity+=1
    sc.save()
    sf.save()
    rwc.save()

buildMarkets()

#test=Market.load("Santa Cruz")
#print(test,test.businesses)
