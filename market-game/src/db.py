from pymongo import MongoClient
client=MongoClient('mongodb+srv://sailor:O9d4*eBJkizk@cluster0-7aeh1.azure.mongodb.net/test?retryWrites=true&w=majority')
marketdb=client.market_test
import socket
local_ip_address=socket.gethostbyname(socket.gethostname())
users=marketdb.users

def getProfile():
    user=users.find_one({'ip': local_ip_address})
    if user is not None:
        from Business import Business
        return Business.load(user['name'])
    else: return None
