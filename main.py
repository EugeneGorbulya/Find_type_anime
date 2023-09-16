import requests
import json
import time
from pprint import pprint
from token import token

TOKEN = token

URL = "https://api.telegram.org/bot" + TOKEN + "/"
URL_ani = "https://kitsu.io/api/edge/anime?filter[categories]="
greeting = "I'm your assistant in the anime search. \nI will send you some titles of anime. \nWrite to start."

data = []

def get_updates():
    r = requests.get(URL + "getUpdates")
    return json.loads(r.text)

def send_text(text, chat_id):
    r = requests.get(URL + "sendMessage?chat_id=" + str(chat_id) + "&text=" + text)
    return json.loads(r.text)

def send_art(art, chat_id):
    r = requests.get(URL + "sendPhoto?chat_id=" + str(chat_id) + "&photo=" + art)
    return json.loads(r.text)

def get_list(text):
    r = requests.get(URL_ani + text)
    return json.loads(r.text)

def working(data):
    message = data['message']
    text = message['text']
    chat = message['chat']
    chat_id = chat['id']
    if text.strip() == "/help":
        send_text(greeting, chat_id)
    else:
        arr = get_list(text)
        for e in arr['data']:
            print(e['attributes']['titles'])
            name = "default"
            for key in list(e['attributes']['titles'].keys()):
                if e['attributes']['titles'][key] is not None:
                    name = e['attributes']['titles'][key]
                    break
            art = e['attributes']['posterImage']['large']
            print(name)
            print(art)
            send_text(name, chat_id)
            send_art(art, chat_id)

data = get_updates()
while True:
    new_data = get_updates()
    if data['result'] != new_data['result']:
        for update in new_data['result'][len(data['result']):]:
            working(update)
            print(update['message']['text'])
        data = new_data
    time.sleep(0.5)
