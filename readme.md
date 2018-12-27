# Language detection bot

This for the Language detection Telegram bot.

## Files
* worker.py: Apply ML and using multithreading asyn message queue to distribute the work.
* bot.py: Communitate with the web server and the Telegram bot, interact with the user input.
* webserver.py: Handle the request from the user input and then distribute the work to the worker and retrive the data returned from worker.

## Model
I'm are using FastText Language Classification(https://fasttext.cc/docs/en/language-identification.html).
Dataset link:https://mycuhk-my.sharepoint.com/:f:/g/personal/1155120122_link_cuhk_edu_hk/EjEs_JdZdlxMn4bFyTQvP7UBZOoM4__wtzeVFSd2bC_sDA?e=pHCelk

## Dependencies and Installation
* redis: `$ sudo yum install redis`
* redis-python: `$ sudo pip install redis`
* telepot: `$ sudo pip install telepot`
* iso639: `$ sudo pip install iso639`
* pandas: `$ sudo pip install pandas`
* flask: `$ sudo pip install flask`
* fastText: `$ sudo pip install fasttext-0.8.22-cp36-cp36m-win_amd64.whl`
fastText link:https://mycuhk-my.sharepoint.com/:f:/g/personal/1155120122_link_cuhk_edu_hk/EjEs_JdZdlxMn4bFyTQvP7UBZOoM4__wtzeVFSd2bC_sDA?e=pHCelk

## Usage
Start all three python script and then talk with Telegram user "@yufei_1_bot" wiht the following commands
* /predict: Input the sentence to be predicted according to the instruction
* /changemodel: Change the model to simple or accurate model
* /history: View all the predict records
* /recent: View recent 5 records