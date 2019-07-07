from pymongo import MongoClient
client=MongoClient('mongodb+srv://sailor:O9d4*eBJkizk@cluster0-7aeh1.azure.mongodb.net/test?retryWrites=true&w=majority')
marketdb=client.market_test
import socket,requests
from multiprocessing import Pool
from requests.exceptions import ConnectionError
from itertools import repeat
import json
local_ip_address=socket.gethostbyname(socket.gethostname())
users=marketdb.users

def getUsers():
    output=[]
    cursor=users.find({})
    for user in cursor:
        output.append(user)
    return output

def getIPList():
    return [user['ip'] for user in getUsers()]

def emit(endpoint,message,ip=None,port=2002):
    url=None
    if ip is None:
        url='http://{}'.format(endpoint)
    else:
        url='http://{}:{}/{}'.format(ip,str(port),endpoint)
    try:
        return requests.post(url,data={'message': message},timeout=5).text
    except ConnectionError as e:
        print("Could not find destination", endpoint,ip)
        return None
        

def broadcast(endpoint,message):
    ips=getIPList()
    res=None
    with Pool(len(ips)) as pool:
        args=zip(repeat(endpoint),repeat(message),ips)
        res=pool.starmap(emit,args)
        
def getProfile():
    user=users.find_one({'ip': local_ip_address})
    if user is not None:
        from Business import Business
        return Business.load(user['name'])
    else: return None

if __name__=='__main__':
    color={
        'x': 0,
        'y': 0,
        'r': 0,
        'g': 0,
        'b': 0,
    }
    broadcast('recievePoint',json.dumps(color))
