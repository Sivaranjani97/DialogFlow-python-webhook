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

from nltk.tokenize import word_tokenize
import nltk
#nltk.download('punkt')
import fileinput
import sys

import pandas as pd
import os.path
import requests
import json

# Flask app should start in global layout
app = Flask(__name__)


# In[ ]:

@app.route('/')
@app.route('/test', methods=['POST'])
def webhook():
    DEVELOPER_ACCESS_TOKEN = '4ac989aab0c14ad7af86386a2d0a2bc5'
    
    stop_words = {'?',
     'a','about', 'above','after','again','against','all','am', 'an','and','any',
     'are','as','at','be', 'because','been','before', 'being','below','between','both','but',
     'by','can','did','do','does','doing','don','down','during','each','few','for','from',
     'further','had','has','have','having','he','her','here','hers','herself','him','himself',
     'his','how','i','if','in','into','is','it','its','itself','just','me','more','most',
     'my','myself','no','nor','not','now','off','on','once','only','or','other','our','ours',
     'ourselves','out','over','own','s','same','she','should','so','some','such','tell','than','that','the',
     'their','theirs', 'them', 'themselves', 'then','there', 'these', 'they', 'this', 'those',
     'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where',
     'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours', 'yourself', 'yourselves'}
    
    #req = request.json
    req = request.get_json(silent=True, force=True)
    #print("Request:")
    
    getIntent = req.get("queryResult").get("intent").get("displayName")
    if(getIntent == "Default Fallback Intent"):
       
        getQuery = req.get("queryResult").get("queryText")
        word_tokens = word_tokenize(getQuery) 
        filtered_sentence = []
 
        for w in word_tokens:
            if w not in stop_words:
            filtered_sentence.append(w)
        

        key = " ".join(filtered_sentence)
        print(key)
        details = ""
        count = 0

        page = urllib.request.urlopen("https://raw.githubusercontent.com/Sivaranjani97/DialogFlow-python-webhook/master/saveetha.doc", data = None)
        content = str(page.readlines())
        list_of_sentences = content.split("\\n")
        for sentence in list_of_sentences:
            sentence.replace('\'','')
            sentence.replace(',','')
            result = sentence.find(key)
            if  sentence.find(key) != -1:
                count = count + 1
                if count <= 2:
                    details += sentence
                else:
                    break
        details = details.replace('\'','')     
        details = details.replace('\\n,', '\n')     
        details = details.replace('\\xa0', ' ')
        details = details.lstrip('\\n\',')
        details = details.rstrip('\\n\',')
        answer = details.strip()
        print(details.strip())

# 1 DEFINE THE URL
        url = 'https://api.dialogflow.com/v1/intents?v=20150910'

# 2 DEFINE THE HEADERS    
        headers = {'Authorization': 'Bearer '+DEVELOPER_ACCESS_TOKEN,'Content-Type': 'application/json'}
        body = {
  "name": key,
  "auto": "true",
  "contexts": [],
  "templates": [
   getQuery ],
  "responses": [
    {
      "resetContexts": "false",
      "action": "",
      "affectedContexts": [
],
      "parameters": [],
      "speech": answer
    }
  ],
  "state": "LOADED",
  "priority": "500000",
  "webhookUsed": "false",
  "webhookForSlotFilling": "false",  "cortanaCommand": {
    "navigateOrService": "NAVIGATE"
  }
}



        data = json.dumps(body,indent = 4 )
        my_result =  {
	      "fulfillmentText": "Sorry i didnt get that",
	       "source": "DialogFlow-python-webhook"
       }
        res = json.dumps(my_result, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

# 4 MAKE THE REQUEST 
       response = requests.post(url,headers=headers,data=data)
       print (response.json)
    
    else:
        intent ="%20".join(getIntent.split(" "))
        print(intent)
        url = 'https://raw.githubusercontent.com/Sivaranjani97/DialogFlow-python-webhook/master/csvfiles/'
        path = url+intent +".csv"
        print(path)
        response = urllib.request.urlopen(path)
        csvfile = csv.reader(codecs.iterdecode(response, 'utf-8'))
        for line in csvfile:
            resp = line[0]
  
       
        
       
	
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
