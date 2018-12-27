#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

import time,requests,telepot,json
from telepot.namedtuple import InlineKeyboardMarkup,InlineKeyboardButton
from telepot.loop import MessageLoop

answered_flag = False
predict_flag = False

def handle(msg):
    global answered_flag
    global predict_flag
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == "text":
        content = msg["text"]
        if (content == "/changemodel"):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Simple', callback_data="{\"data\":\"Simple\"}"),
                 InlineKeyboardButton(text='Accurate', callback_data="{\"data\":\"Accurate\"}")]
            ])
            bot.sendMessage(chat_id, 'Which model would you like to use?', reply_markup=keyboard)
            answered_flag = False
        elif (content == "/predict"):
            bot.sendMessage(chat_id, 'Please input the sentence you want to predict')
            predict_flag = True
        elif (content == "/recent"):
            response = requests.post("http://127.0.0.1:8080/recent_five", data = json.dumps({"chat_id": str(chat_id)}))
            if response.text == "{}":
                bot.sendMessage(chat_id, "Your have not predict yet.")
            else:  
                json_data = json.loads(response.text)
                message = ""
                for key, value in json_data.items():
                    message = message + "sentence: " + value['data'] + "; language: " + value['language'] + "\n"
                bot.sendMessage(chat_id, "Your recent 5 predict:")
                bot.sendMessage(chat_id, message)
        elif (content == "/history"): 
            response = requests.post("http://127.0.0.1:8080/history", data = json.dumps({"chat_id": str(chat_id)}))
            if response.text == "{}":
                bot.sendMessage(chat_id, "Your have not predict yet.")
            else:
                json_data = json.loads(response.text)
                message = ""
                for key, value in json_data.items():
                    message = message + "sentence: " + value['data'] + "; language: " + value['language'] + "\n"
                bot.sendMessage(chat_id, "Your all history predict:")
                bot.sendMessage(chat_id, message)
        else:
            if (predict_flag):
                response = requests.post("http://127.0.0.1:8080/predict", data = json.dumps({"chat_id": str(chat_id),"data": content}))
                json_data = json.loads(response.text)
                language = json_data.get("language")
                bot.sendMessage(chat_id, "The language used in the sentence is " + language)
                predict_flag = False
            else:
                bot.sendMessage(chat_id, "Unknown Command! To predict language, please input the command /predict")

def on_callback_query(msg):
    global answered_flag
    global predict_flag
    # the rate can only be answered once
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    if(answered_flag == True):
        bot.answerCallbackQuery(query_id, text='You have change the model! For change the model again, please type command /changemodel')
    else:
        json_data = json.loads(query_data)
        answered_flag = True
        response = requests.post("http://127.0.0.1:8080/change_model", data = json.dumps({"model_type": json_data.get("data")}))
        json_data = json.loads(response.text)
        if json_data.get("status") == "1":
            bot.answerCallbackQuery(query_id, text='Change model success!')
        else:
            bot.answerCallbackQuery(query_id, text='System error! Please try again!')
if __name__ == "__main__":
    # Provide your bot's token
    bot = telepot.Bot("787863087:AAE8fUa16n9lMxMTFNEwuN6zoYJORlC7MTE")
    MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()
    while True:
        time.sleep(10)

