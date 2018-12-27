#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json,fastText,os
from redis import StrictRedis
from flask import Flask, request, jsonify

app = Flask(__name__)
    
@app.route('/change_model',methods=["POST"])
def f_change_model():
    global model
    data = request.get_data()
    json_data = json.loads(data)
    model_type = json_data.get("model_type")
    
    r = StrictRedis(host='localhost', port=6379)
    r.rpush('channel_c', model_type)
    
    return "{\"status\":\"1\"}"

@app.route('/predict',methods=["POST"])
def f_predict():
    data = request.get_data()
    json_data = json.loads(data)
    data = json_data.get("data")
    
    r = StrictRedis(host='localhost', port=6379)
    r.rpush('channel_p', data.encode("utf-8"))
    item = r.blpop('channel_p_back')
    language = item[1].decode("utf-8")
    
    json_data["language"] = language
    r.rpush('channel_rc', str(json_data).encode("utf-8"))
    
    return "{\"status\":\"1\",\"language\":\"" + language + "\"}"

@app.route('/recent_five',methods=["POST"])
def f_recent_five():
    data = request.get_data()
    json_data = json.loads(data)
    chat_id = json_data.get("chat_id")
    
    r = StrictRedis(host='localhost', port=6379)
    r.rpush('channel_r', chat_id.encode("utf-8"))
    item = r.blpop('channel_r_back')
    print("send res")
    return item[1]

@app.route('/history',methods=["POST"])
def f_history():
    data = request.get_data()
    json_data = json.loads(data)
    chat_id = json_data.get("chat_id")
    
    r = StrictRedis(host='localhost', port=6379)
    r.rpush('channel_h', chat_id.encode("utf-8"))
    item = r.blpop('channel_h_back')
    print("send his")
    return item[1]

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

