from flask import Flask, request, jsonify, render_template,redirect
from flask_restful import Resource,Api
from flask_pymongo import PyMongo
from Market import Market
from Business import Business
import os,random,requests
from db import local_ip_address,users,marketdb,getProfile,getIPList,getUsers
from flask_socketio import SocketIO,send,emit
app=Flask(__name__)
api=Api(app)
app.config['MONGO_DBNAME']='market_test'
app.config['MONGO_URI'] = 'mongodb+srv://sailor:O9d4*eBJkizk@cluster0-7aeh1.azure.mongodb.net/test?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

canvas=marketdb.canvas

@socketio.on('new')
def setPoint(x,y,r,g,b):
    color={
        'x': x,
        'y': y,
        'r': r,
        'g': g,
        'b': b,
    }
    emit('new',color,namespace='/', broadcast=True)
    return canvas.update_one({'x': x, 'y': y}, {'$set': color},upsert=True)


@app.route('/', methods=['GET'])
def gotoCanvas():
    return redirect("/canvas")


@app.route('/recieve', methods=['POST'])
def log():
    print(request.values.get('message'))
    return "Success"

@app.route('/canvas', methods=['POST'])
def set_pixel():
    marketName=request.values.get('name')
    try:
        red=int(request.values.get('red'))
        blue=int(request.values.get('blue'))
        green=int(request.values.get('green'))
        x=int(request.values.get('x'))
        y=int(request.values.get('y'))
    except Exception as e:
        print("ERROR",e)
        return redirect('/canvas')
    print(red,blue,green,x,y)
    business=Business.load(marketName)
    price=1
    colors=[]
    if red > 0:
        colors.append('Red')
    if blue > 0:
        colors.append('Blue')
    if green > 0:
        colors.append('Green')
        
    for color in colors:
        if business.stock[color].quantity<0:
            print("Not enough pigment!")
            return redirect('/canvas')

    paid=False
    for color in colors:
        business.stock[color].quantity-=1
        paid=True
        
    if colors==[]:
        for name,stock in business.stock.items():
            if stock.quantity > 0:
                stock.quantity-=1
                paid=True
                break
                
    if paid:
        setPoint(x,y,red,green,blue)
        business.save()
    else:
        print("not enough money")
    return redirect('/canvas')

@app.route('/canvas', methods=['GET'])
def get_canvas():
    size=25
    colors=canvas.find({})
    colorMap={}
    t=lambda i: int(255.0*i/100.0)
    for color in colors:
        colorMap[(int(color['x']),int(color['y']))]=(t(color['r']),t(color['g']),t(color['b']))
    profile=getProfile()
    return render_template('canvas.html',colors=colorMap,x=range(size),y=range(size),size=size,profile=profile) 
    
@app.route('/market', methods=['GET'])
def viewMarket():
    marketName=request.args.get('name')
    market=Market.load(marketName)
    print(market)
    return render_template('market.html',market=market.data(),businesses=market.businesses)



if __name__=="__main__":
    socketio.run(app,host='0.0.0.0',port='2002',debug=True)
        
