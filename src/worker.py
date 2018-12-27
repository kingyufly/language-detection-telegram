#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ast,json,fastText,os,threading
import pandas as pd
from iso639 import languages
from redis import StrictRedis

global model

def worker_model(arg):
    global model
    r = StrictRedis(host='localhost', port=6379)

    while True:
        item = r.blpop('channel_c')
        data = item[1].decode("utf-8")
        if data == "Accurate":
            model = fastText.load_model('lid.176.bin')
        else:
            model = fastText.load_model('lid.176.ftz')

def worker_predict(arg):
    global model
    r = StrictRedis(host='localhost', port=6379)

    while True:
        item = r.blpop('channel_p')
        data = item[1].decode("utf-8")
        label,result = model.predict(data)
        result = languages.get(alpha2=label[0][9:]).name
        r.rpush('channel_p_back', result.encode("utf-8"))

def worker_recorder(arg):
    r = StrictRedis(host='localhost', port=6379)

    while True:
        item = r.blpop('channel_rc')
        dict_data = item[1].decode("utf-8")
        
        dict_data = ast.literal_eval(dict_data)
        chat_id = dict_data['chat_id']
        data = dict_data['data']
        language = dict_data['language']

        if os.path.exists(chat_id + ".csv"): 
            df = pd.read_csv(chat_id + ".csv")
            df = df.append({'data': data,'language': language}, ignore_index=True)
        else:
            df = pd.DataFrame({'data': [data],'language': [language]})
        
        df.to_csv(chat_id + ".csv",index=False)
    
def worker_recent(arg):
    r = StrictRedis(host='localhost', port=6379)

    while True:
        item = r.blpop('channel_r')
        chat_id = item[1].decode("utf-8")

        if os.path.exists(chat_id + ".csv"): 
            df = pd.read_csv(chat_id + ".csv")
            df.sort_index(inplace = True, ascending = False)
            df = df.head()
            r.rpush('channel_r_back', df.to_json(orient='index').encode("utf-8"))
        else:
            r.rpush('channel_r_back', "{}".encode("utf-8"))
    
def worker_history(arg):
    r = StrictRedis(host='localhost', port=6379)

    while True:
        item = r.blpop('channel_h')
        chat_id = item[1].decode("utf-8")

        if os.path.exists(chat_id + ".csv"): 
            df = pd.read_csv(chat_id + ".csv")
            df.sort_index(inplace = True, ascending = False)
            r.rpush('channel_h_back', df.to_json(orient='index').encode("utf-8"))
        else:
            r.rpush('channel_h_back', "{}".encode("utf-8"))

    
threads = []
m1 = threading.Thread(target = worker_model, args = ('m1',))
threads.append(m1)
m2 = threading.Thread(target = worker_model, args = ('m2',))
threads.append(m2)   
    
p1 = threading.Thread(target = worker_predict, args = ('p1',))
threads.append(p1)
p2 = threading.Thread(target = worker_predict, args = ('p2',))
threads.append(p2)

rc1 = threading.Thread(target = worker_recorder, args = ('rc1',))
threads.append(rc1)
rc2 = threading.Thread(target = worker_recorder, args = ('rc2',))
threads.append(rc2)

r1 = threading.Thread(target = worker_recent, args = ('r1',))
threads.append(r1)
r2 = threading.Thread(target = worker_recent, args = ('r2',))
threads.append(r2)

h1 = threading.Thread(target = worker_history, args = ('h1',))
threads.append(h1)
h2 = threading.Thread(target = worker_history, args = ('h2',))
threads.append(h2)

if __name__ == '__main__':
    model = fastText.load_model('lid.176.ftz')
    for t in threads:
        t.setDaemon(True)
        t.start()


# In[ ]:




