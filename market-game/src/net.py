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

canvas=marketdb.canvas
def setPoint(x,y,r,g,b):
    color={
        'x': x,
        'y': y,
        'r': r,
        'g': g,
        'b': b,
    }
    return canvas.update_one({'x': x, 'y': y}, {'$set': color},upsert=True)

@app.route('/canvas', methods=['POST'])
def set_pixel():
    marketName=request.values.get('name')
    try:
        red=int(request.values.get('red'))
        blue=int(request.values.get('blue'))
        green=int(request.values.get('green'))
        x=int(request.values.get('x'))
        y=int(request.values.get('y'))
        print(red,blue,green,x,y)
        business=Business.load(marketName)
        price=1
        if business.quantity>=price:
            business.quantity-=price
            setPoint(x,y,red,green,blue)
            business.save()
        else:
            print("not enough money")
    except Exception as e:
        print(e)
    return redirect('/canvas')

@app.route('/canvas', methods=['GET'])
def get_canvas():
    size=50
    cs=sorted(css,key=lambda a: a['index'])
    colors=[(c['r'],c['g'],c['b']) for c in cs]
    print(colors[0])
    me=users.find_one({'ip': local_ip_address})
    profile=None
    if me is not None:
        profile=marketdb.business.find_one({'name': me['name']})
        print(profile)
    return render_template('canvas.html',colors=colors,x=range(size),y=range(size),size=size,user=me,profile=profile) 
    
@app.route('/market', methods=['GET'])
def viewMarket():
    marketName=request.args.get('name')
    market=Market.load(marketName)
    print(market)
    return render_template('market.html',market=market.data(),businesses=market.businesses)



if __name__=="__main__":
    app.run(port='2002',debug=True)
    
