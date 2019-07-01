import bson
class Saveable:
    def __init__(self):
        self._id=None
    def load(d,db):
        obj=None
        if issubclass(str,type(d)):
            obj=db.find_one({'name': d})
        elif issubclass(bson.objectid.ObjectId,type(d)):
            obj=db.find_one({'_id': d})
        return obj
    def getId(name,db):
        response=db.find_one({'name': name})
        if response is not None:
            return response['_id']
        else: return None
    def data():
        return {'name': 'Aurther'}
    def save(self,db,v=True):
        data=self.data()
        db.update({'name': self.name},{'$set': data},upsert=True)
        self._id=db.find_one({'name': self.name})['_id']
        print("Successful save of",self)
