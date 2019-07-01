#Script used for building the environment.
from pymongo import MongoClient
from Market import Market
from Business import Business #cluster0-7aeh1.azure.mongodb.net
client=MongoClient('mongodb+srv://sailor:O9d4*eBJkizk@cluster0-7aeh1.azure.mongodb.net/test?retryWrites=true&w=majority')
marketdb=client.market_test
business=marketdb.business
market=marketdb.market

sc=Market("Santa Cruz", (5,0))
nike=Business("Nike",sc,100,10)
addidas=Business("Addidas",sc,77,33)
sc.save()

test=Market.load("Santa Cruz")
print(test,test.businesses)
