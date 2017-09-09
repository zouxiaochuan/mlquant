import uwsgi;
from flask import Flask;
from flask import request;
import json;
import pymongo;
from pymongo import MongoClient;


db = MongoClient('mongodb://xxxx:xxxx@localhost:27017/')['mlquant'];
app=Flask(__name__);

@app.route('/uploadScore',methods=['POST'])
def uploadScore():
    jsonstr = request.stream.read();
    inputs = json.loads(jsonstr);
    
    db.insert_many(inputs);
    return json.dumps({'success':True});

@app.route('/queryScore',methods=['POST'])
def queryScore():
    qstr = request.stream.read();
    qres = list(db.find(json.loads(qstr)));
    ret = dict();
    ret['success'] = True;
    ret['data'] = qres;

    return json.dumps(ret);
