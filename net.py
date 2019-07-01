from flask import Flask, request, jsonify, render_template
from flask_restful import Resource,Api
from flask_pymongo import PyMongo
from Market import Market
import os
app=Flask(__name__)
api=Api(app)
app.config['MONGO_DBNAME']='market_test'
app.config['MONGO_URI'] = 'mongodb+srv://sailor:O9d4*eBJkizk@cluster0-7aeh1.azure.mongodb.net/test?retryWrites=true&w=majority'

@app.route('/business/bidprice', methods=['POST'])
def set_bidprice():
    pass
    

@app.route('/market', methods=['GET'])
def viewMarket():
    marketName=request.args.get('name')
    market=Market.load(marketName)
    print(market)
    return render_template('market.html',market=market.data(),businesses=market.businesses)




if __name__=="__main__":
    app.run(port='2002',debug=True)
