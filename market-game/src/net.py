from flask import Flask, request, jsonify, render_template,redirect
from flask_restful import Resource,Api
from flask_pymongo import PyMongo
from Market import Market
from Business import Business
import os,random
from db import local_ip_address,users,marketdb
app=Flask(__name__)
api=Api(app)
app.config['MONGO_DBNAME']='market_test'
app.config['MONGO_URI'] = 'mongodb+srv://sailor:O9d4*eBJkizk@cluster0-7aeh1.azure.mongodb.net/test?retryWrites=true&w=majority'

@app.route('/canvas', methods=['POST'])
def set_pixel():
    marketName=request.values.get('name')
    business=Business.load(marketName)
    business.quantity-=1
    business.save()
    return redirect('/canvas')
@app.route('/canvas', methods=['GET'])
def get_canvas():
    colors=[]
    for i in range(100):
        for j in range(100):
            r=int(random.random()*256)
            g=int(random.random()*256)
            b=int(random.random()*256)
            colors.append((r,g,b))
    me=users.find_one({'ip': local_ip_address})
    profile=None
    if me is not None:
        profile=marketdb.business.find_one({'name': me['name']})
        print(profile)
    return render_template('canvas.html',colors=colors,x=range(100),y=range(100),size=100,user=me,profile=profile) 
    
@app.route('/market', methods=['GET'])
def viewMarket():
    marketName=request.args.get('name')
    market=Market.load(marketName)
    print(market)
    return render_template('market.html',market=market.data(),businesses=market.businesses)



if __name__=="__main__":
    app.run(port='2002',debug=True)
    
