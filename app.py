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


# firebase
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ithbtest.firebaseio.com'
})

# Flask app should start in global layout
app = Flask(__name__)

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
    a = req.get("id")
    return {
            "speech": a,
            "displayText": a,
            #"data": {},
            #"contextOut": [],
            "source": a
        }
        
        
if __name__ == '__main__':
    port = int(os.getenv('PORT', 4040))

    print ("Starting app on port %d" %(port))

    app.run(debug=False, port=port, host='0.0.0.0')
