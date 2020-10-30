from django.conf import settings
import logging
import re
import requests
from requests.auth import AuthBase
import base64
import hashlib
import json
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)
monnify_api_key = settings.MONNIFY_API_KEY
monnify_secret_key = settings.MONNIFY_SECRET_KEY
monnify_contract_code = settings.MONNIFY_CONTRACT_CODE
monnify_currency_code = settings.MONNIFY_CURRENCY_CODE
MONNIFY_URL_PREFIX = settings.MONNIFY_BASEURL_PREFIX

MONNIFY_URLS = {'login':MONNIFY_URL_PREFIX +'monnify.com/api/v1/auth/login',
                'account_reservation':MONNIFY_URL_PREFIX +'monnify.com/api/v1/bank-transfer/reserved-accounts',
                'get_transaction':MONNIFY_URL_PREFIX +'monnify.com/api/v1/merchant/transactions/query',
                    }

class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token=None, auth_type='Bearer', custom_header=None, Content_Type='application/json'):
        self.token = token
        self.auth_type = auth_type
        self.custom_header = custom_header
        self.Content_Type = Content_Type

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers['Content-Type'] = self.Content_Type
        if self.token is not None:
            if self.custom_header is None:
                #print(f'{self.auth_type} {self.token}',' from services')
                r.headers['Authorization'] = f'{self.auth_type} {self.token}'  # Python 3.6+
            else:
                r.headers[self.custom_header] = f'{self.token}'
            #print(r.headers,'rrrrrrrrr')
        return r

class ExtendedRequests:
    headers = {'Content-Type': 'application/json',}
    @classmethod
    def post_data(cls,api_url,token=None,token_data=dict(),**data):
        if not data:
            data = dict()
        if token:
            response = requests.post(api_url,json=data,auth=TokenAuth(token,**token_data))
        else:
            response = requests.post(api_url,json=data,headers=cls.headers)
       
        resp_data = json.loads(response.content.decode('utf-8'))
        code = response.status_code
        return code, resp_data
    @classmethod
    def get_data(cls,api_url,token=None,token_data=dict(),**data):
        if not data:
            if token:
                response = requests.get(api_url,auth=TokenAuth(token,**token_data))
            else:
                response = requests.get(api_url,headers=cls.headers)
        else:
            if token:
                response = requests.get(api_url,params=data,auth=TokenAuth(token,**token_data))
            else:
                response = requests.get(api_url,params=data,headers=cls.headers)
        resp_data = json.loads(response.content.decode('utf-8'))
        code = response.status_code
        return code, resp_data

def hashKey(**kwargs):
    text = kwargs['clientSecret']+'|'+kwargs['paymentReference']+'|'+kwargs['amountPaid']+'|'+kwargs['paidOn']+'|'+kwargs['transactionReference']
    byte_text = bytes(text, 'utf8')
    hashtext = hashlib.sha512(byte_text).hexdigest()
    return hashtext

def generate_monnify_token(**kwargs):
    text = f'{monnify_api_key}:{monnify_secret_key}'
    byte_text = bytes(text, 'utf8')
    encoded = base64.b64encode(byte_text)
    keys_encoded2 = encoded.decode()
    if kwargs:
        return 200,keys_encoded2
    result = ExtendedRequests.post_data(MONNIFY_URLS['login'],keys_encoded2,token_data={'auth_type':'Basic'},**kwargs)
    return result[0],result[1]['responseBody']['accessToken']

class ExtendedRequests2:
    headers = {'Content-Type': 'application/json',}
    
    @classmethod
    def get_data(cls,api_url,token=None,token_data=dict(),**data):
        if not data:
            if token:
                response = requests.get(api_url,auth=TokenAuth(token,**token_data))
            else:
                response = requests.get(api_url,headers=cls.headers)
        else:
            if token:
                response = requests.get(api_url,auth=TokenAuth(token,**token_data))
            else:
                response = requests.get(api_url,params=data,headers=cls.headers)
    
        resp_data = json.loads(response.content.decode('utf-8'))
        code = response.status_code
        return code, resp_data