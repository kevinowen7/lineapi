#!/usr/bin/env python


import json
import os
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

from flask import Flask
from flask import request
from flask import make_response

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# firebase
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ithbtest.firebaseio.com'
})

# Flask app should start in global layout
app = Flask(__name__)

line_bot_api = LineBotApi('fHIvKaGYZfXuMVXMt/tG1WpFztLQYqzlhDp5DB/Memvyo7TfrObM2bpXTS/W1jwlWsQulRJylBl3seFXcWr10Zu2SJldz8Qxd5sdBxxEQa3uXvxKNhU84K8CLYQ4yFstk2dhUdjEkdkMyzbzfgUHwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0d184e88d0b01d9a5586b06abd6a1250')

@app.route('/webhook', methods=['POST'])


def webhook():
    req = request.get_json(silent=True, force=True)
    res = makeWebhookResult(req)  
    
    res = json.dumps(res, indent=4)
    print(res)
    res2 = {
            "speech": "tgl2",
            "displayText": "tgl2",
            #"data": {},
            #"contextOut": [],
            "source": "tgl2"
        }
    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    
    return r




def makeWebhookResult(req):  
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    return {
            "speech": "w",
            "displayText": "w",
            #"data": {},
            #"contextOut": [],
            "source": "w"
        }
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    w = handler.handle(body, signature)
    return {
            "speech": w,
            "displayText": w,
            #"data": {},
            #"contextOut": [],
            "source": w
        }
        
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    return event.resource.userId
    
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 4040))

    print ("Starting app on port %d" %(port))

    app.run(debug=False, port=port, host='0.0.0.0')
