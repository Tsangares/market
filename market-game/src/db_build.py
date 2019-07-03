from db import marketdb
def setPoint(db,x,y,r,g,b,index=0):
    color={
        'x': x,
        'y': y,
        'r': r,
        'g': g,
        'b': b,
        'index': index,
    }
    return db.update_many({'x': x, 'y': y}, {'$set': color},upsert=True)

def buildCanvas(db,hue=10,size=50):
    _index=0
    for i in range(size):
        for j in range(size):
            _index+=1
            print(i,j,setPoint(db,i,j,hue,hue,hue,_index))
canvas=marketdb.canvas
buildCanvas(canvas,70,25)


