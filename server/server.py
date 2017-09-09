import uwsgi;
from flask import Flask;
from flask import request;
import json;
import pymongo;
from pymongo import MongoClient;


app=Flask(__name__);

def getdb():
    return MongoClient('mongodb://xiaochuan:iphoipho0@localhost:27017/')['mlquant']['scores'];

@app.route('/uploadScore',methods=['POST'])
def uploadScore():
    db = getdb();
    jsonstr = request.stream.read();
    inputs = json.loads(jsonstr);

    for rec in inputs:
        rec['_id'] = rec['secID']+'_'+rec['tradeDate'];
        db.update({"_id":rec['_id']},
                   rec,
                   upsert=True
        );
        pass;
    
    return json.dumps({'success':True});

@app.route('/queryScore',methods=['POST'])
def queryScore():
    db = getdb();
    qstr = request.stream.read();
    qres = list(db.find(json.loads(qstr)));
    ret = dict();
    ret['success'] = True;
    ret['data'] = qres;

    return json.dumps(ret);
