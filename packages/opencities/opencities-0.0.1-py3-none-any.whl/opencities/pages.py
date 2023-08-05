# IMPORT PACKAGES
import uuid
import math
import hmac
import hashlib
import base64
import requests
import json
from urllib import parse
from datetime import datetime, timedelta

# GET PAGES FROM OPENCITIES API
# Build Function to Get Data
def oc_api(url, api_key, app_id, method='GET', body='', output='json'):
    # Authentication Hash
    method = method.upper()
    nonce = str(uuid.uuid4()).replace('-', '')[0:8]
    timestamp = math.floor((datetime.now() + timedelta(hours=5) - datetime.strptime('1970-01-01', '%Y-%m-%d')).total_seconds())
    if body == '':
        message = str(str(app_id)
                      + str(method)
                      + str(parse.quote(url, safe='').lower())
                      + str(timestamp)
                      + str(nonce)
                      + str(''))
    else:
        message = str(str(app_id)
                      + str(method)
                      + str(parse.quote(url, safe='').lower())
                      + str(timestamp)
                      + str(nonce)
                      + str(base64.b64encode(bytes(str(json.dumps(body)), 'utf-8')).decode()))
    signature = base64.b64encode(hmac.new(bytes(api_key, 'utf-8'),
                                          bytes(message, 'utf-8'),
                                          digestmod=hashlib.sha256).digest()
                                 ).decode()
    auth = 'hmac ' + str(app_id) + ':' + signature + ':' + str(nonce) + ':' + str(timestamp)

    if method == 'GET':
        r = requests.get(url=url,
                         headers={'Accept': 'application/json',
                                  'Authorization': auth}
                         )
    elif method == 'POST':
        r = requests.post(url=url,
                          data=json.dumps(body),
                          headers={'Content-Type': 'application/json',
                                   'Accept': 'application/json',
                                   'Authorization': auth}
                          )
    else:
        r = requests.delete(url=url,
                            data=body,
                            headers={'Accept': 'application/json',
                                     'Authorization': auth})
    return r