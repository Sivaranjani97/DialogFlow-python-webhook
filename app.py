
# coding: utf-8

# In[1]:


import urllib
import json
import os
import sys

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


# In[ ]:


@app.route('/test', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    my_result =  {
        "speech": speech,
        "displayText": speech,
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
