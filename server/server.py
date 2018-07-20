import uwsgi;
from flask import Flask;
from flask import request;
import json;
import pymongo;
from pymongo import MongoClient;


app=Flask(__name__);

def getdb():
    return MongoClient('mongodb://xiaochuan:iphoipho0@localhost:27017/')['mlquant']['scores'];

def getMaxTradeDate(db):
    return db.aggregate([{ '$group' : { '_id': 'null', 'max': { '$max' : '$tradeDate' }}}]).next()['max'];

def getScores(db,query):
    scores =  list(db.find(query).sort('score',pymongo.DESCENDING));
    for sc in scores:
        sc.pop('_id');
        pass;
    return scores;

@app.route('/uploadScore',methods=['POST'])
def uploadScore():
    db = getdb();
    jsonstr = request.stream.read();
    inputs = json.loads(jsonstr);
    dts = {rec['tradeDate'] for rec in inputs};
    for dt in dts:
        db.delete_many({'tradeDate':dt});
        pass;

    for rec in inputs:
        rec['_id'] = rec['secID']+'_'+rec['tradeDate'];
        db.update({"_id":rec['_id']},
                   rec,
                   upsert=True
        );
        pass;
    
    return json.dumps({'success':True});

@app.route('/queryScore',methods=['GET','POST'])
def queryScore():
    db = getdb();
    if request.method=='GET':
        query = {'tradeDate':getMaxTradeDate(db)};
        pass;
    elif request.method=='POST':
        query = json.loads(request.stream.read());
        pass;

    qres = getScores(db,query);
    ret = dict();
    ret['success'] = True;
    ret['data'] = qres;

    return json.dumps(ret);
