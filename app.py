# coding: utf-8

# In[1]:

import urllib
import json
import os
import sys
import csv
import urllib.request
import codecs

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


# In[ ]:

@app.route('/')
@app.route('/test', methods=['POST'])
def webhook():
    
    #req = request.json
    req = request.get_json(silent=True, force=True)
    #print("Request:")
    
    getIntent = req.get("queryResult").get("intent").get("displayName")
    intent ="%20".join(getIntent.split(" "))
    print(intent)
    url = 'https://raw.githubusercontent.com/Sivaranjani97/DialogFlow-python-webhook/master/csvfiles/'
    path = url+intent +".csv"
    print(path)
    response = urllib.request.urlopen(path)
    csvfile = csv.reader(codecs.iterdecode(response, 'utf-8'))
    for line in csvfile:
        resp = line[0]
       # print(resp)
   # url = 'https://raw.githubusercontent.com/Sivaranjani97/DialogFlow-python-webhook/master/Serge%20Kampf.csv'
    #response = urllib.request.urlopen(url)
   # csvfile = csv.reader(codecs.iterdecode(response, 'utf-8'))
    #for line in csvfile:
      #  resp = line[0]
        
       
	
    my_result =  {
	"fulfillmentText": resp,
	"source": "DialogFlow-python-webhook"
       }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5002))

	print("Starting app on port %d" % port)

	app.run(debug=True, port=port, host='0.0.0.0')
