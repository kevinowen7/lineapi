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
    if req.get("result").get("action") == "test":
        result0 = req.get("result")
        result = result0.get("resolvedQuery")
        d = result0.get("parameters")
        database = db.reference()
        thn = int(result.split("/")[2].split(" ")[0])
        bln = int(result.split("/")[1])
        tgl = int(result.split("/")[0])
        lt = d.get("lantai")
        x=1
        hasillist=[]
        hasil = database.child(str(thn)+"/"+str(bln)+"/"+str(tgl)+"/lantai:"+str(lt)).get()
        if hasil==None:
            return {
                "speech": "lantai "+str(lt)+" tidak ada jadwal hari ini",
                "displayText": "lantai "+str(lt)+" tidak ada jadwal hari ini",
                #"data": {},
                #"contextOut": [],
                "source": "lantai "+str(lt)+" tidak ada jadwal hari ini"
            }
        while(x<len(hasil)):
            print(hasil[x])
            if hasil[x]["Nama Dosen"]==" ":
                hasillist.append("Jam: "+hasil[x]["Jam"]+"\n"+"Mata Kuliah: "+hasil[x]["Mata Kuliah"]+"\n"+"Ruangan: "+hasil[x]["Ruang"]+"\n"+"\n"+"\n")
            else:
                hasillist.append("Jam: "+hasil[x]["Jam"]+"\n"+"Mata Kuliah: "+hasil[x]["Mata Kuliah"]+"\n"+"Nama Dosen: "+hasil[x]["Nama Dosen"]+"\n"+"Ruangan: "+hasil[x]["Ruang"]+"\n"+"\n"+"\n")

            x=x+1
        print(len(hasillist))
        if len(hasillist)==0:
            return {
                "speech": "lantai "+str(lt)+" tidak ada jadwal hari ini",
                "displayText": "lantai "+str(lt)+" tidak ada jadwal hari ini",
                #"data": {},
                #"contextOut": [],
                "source": "lantai "+str(lt)+" tidak ada jadwal hari ini"
            }
        r=""
        for i in hasillist:
            r=r+i
            
        return{"speech": "",
           "messages": [
            {
              "type": 0,
              "speech": ""
            },
            {
          "type": 4,
          "payload": {
             "line": {
                "type": "flex",
                "altText": "this is a flex message",
                "contents": {
                 "type": "bubble",
                  "body": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "text",
                        "text": r,
                        "wrap": True
                      }
                    ]
                  }
                 }
             }
          }
          }
            ]
        }
        
    if req.get("result").get("action") == "dosen":
        result0 = req.get("result")
        result = result0.get("resolvedQuery")
        d = result0.get("parameters")
        thn = int(result.split("/")[2].split(" ")[0])
        bln = int(result.split("/")[1])
        tgl = int(result.split("/")[0])
        dosen = d.get("any")
        
        database = db.reference()
        hasil = database.child(str(thn)+"/"+str(bln)+"/"+str(tgl)).get()
        if hasil==None:
            return {
                "speech": dosen+" tidak ada jadwal hari ini",
                "displayText": dosen+" tidak ada jadwal hari ini",
                #"data": {},
                #"contextOut": [],
                "source": dosen+" tidak ada jadwal hari ini"
            }
        lt=1
        hasillist=[]
        while(lt<len(hasil)+1):
            x=1
            try:
                while(x<len(hasil["lantai:"+str(lt)])):
                    if(dosen.lower() in hasil["lantai:"+str(lt)][x]["Nama Dosen"].lower()) or (dosen.lower() in hasil["lantai:"+str(lt)][x]["Mata Kuliah"].lower()):
                        if hasil["lantai:"+str(lt)][x]["Nama Dosen"]==" ":
                            hasillist.append("Jam: "+hasil["lantai:"+str(lt)][x]["Jam"]+"\n"+"Mata Kuliah: "+hasil["lantai:"+str(lt)][x]["Mata Kuliah"]+"\n"+"Ruangan: "+hasil["lantai:"+str(lt)][x]["Ruang"]+"\n"+"\n"+"\n")                
                        else:
                            hasillist.append("Jam: "+hasil["lantai:"+str(lt)][x]["Jam"]+"\n"+"Mata Kuliah: "+hasil["lantai:"+str(lt)][x]["Mata Kuliah"]+"\n"+"Nama Dosen: "+hasil["lantai:"+str(lt)][x]["Nama Dosen"]+"\n"+"Ruangan: "+hasil["lantai:"+str(lt)][x]["Ruang"]+"\n"+"\n"+"\n")
                    print(hasil["lantai:"+str(lt)][x]["Nama Dosen"])
                    x=x+1
                lt=lt+1
            except Exception as res:
                lt=lt+1
        if len(hasillist)==0:
            return {
                "speech": dosen+" tidak ada jadwal hari ini",
                "displayText": dosen+" tidak ada jadwal hari ini",
                #"data": {},
                #"contextOut": [],
                "source": dosen+" tidak ada jadwal hari ini"
            }
        r=""
        for i in hasillist:
            r=r+i
        return {
            "speech": r,
            "displayText": r,
            #"data": {},
            #"contextOut": [],
            "source": r
        }
    
    if req.get("result").get("action") == "ruang":
        result0 = req.get("result")
        result = result0.get("resolvedQuery")
        d = result0.get("parameters")
        thn = int(result.split("/")[2].split(" ")[0])
        bln = int(result.split("/")[1])
        tgl = int(result.split("/")[0])
        ruang = d.get("any")
        
        database = db.reference()
        hasil = database.child(str(thn)+"/"+str(bln)+"/"+str(tgl)).get()
        if hasil==None:
            return {
                "speech": "Ruangan "+ruang+" tidak ada jadwal hari ini",
                "displayText": "Ruangan "+ruang+" tidak ada jadwal hari ini",
                #"data": {},
                #"contextOut": [],
                "source": "Ruangan "+ruang+" tidak ada jadwal hari ini"
            }
        
        lt=1
        hasillist=[]
        while(lt<len(hasil)+1):
            x=1
            try:
                while(x<len(hasil["lantai:"+str(lt)])):
                    if(ruang.lower() in hasil["lantai:"+str(lt)][x]["Ruang"].lower()):
                        if hasil["lantai:"+str(lt)][x]["Nama Dosen"]==" ":
                            hasillist.append("Jam: "+hasil["lantai:"+str(lt)][x]["Jam"]+"\n"+"Mata Kuliah: "+hasil["lantai:"+str(lt)][x]["Mata Kuliah"]+"\n"+"Ruangan: "+hasil["lantai:"+str(lt)][x]["Ruang"]+"\n"+"\n"+"\n")                
                        else:
                            hasillist.append("Jam: "+hasil["lantai:"+str(lt)][x]["Jam"]+"\n"+"Mata Kuliah: "+hasil["lantai:"+str(lt)][x]["Mata Kuliah"]+"\n"+"Nama Dosen: "+hasil["lantai:"+str(lt)][x]["Nama Dosen"]+"\n"+"Ruangan: "+hasil["lantai:"+str(lt)][x]["Ruang"]+"\n"+"\n"+"\n")
                    print(hasil["lantai:"+str(lt)][x]["Nama Dosen"])
                    x=x+1
                lt=lt+1
            except Exception as res:
                lt=lt+1
        
        if len(hasillist)==0:
            return {
                "speech": "Ruangan "+ruang+" tidak ada jadwal hari ini",
                "displayText": "Ruangan "+ruang+" tidak ada jadwal hari ini",
                #"data": {},
                #"contextOut": [],
                "source": "Ruangan "+ruang+" tidak ada jadwal hari ini"
            }
        r=""
        for i in hasillist:
            r=r+i
        return {
            "speech": r,
            "displayText": r,
            #"data": {},
            #"contextOut": [],
            "source": r
        }
        
        
if __name__ == '__main__':
    port = int(os.getenv('PORT', 4040))

    print ("Starting app on port %d" %(port))

    app.run(debug=False, port=port, host='0.0.0.0')
