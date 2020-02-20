"""
 ******************************************************************************
 *  Purpose: Login Registration functionality using Django-REST framework.
 *  File  : token.py
 *  Author :Santoshi kalaskar
 ******************************************************************************
"""


import datetime
import pdb
import jwt
import requests
from Fundooo.settings import SECRET_KEY, AUTH_ENDPOINT

def token_activation(username,password):

    data = {
        'username': username,
        'password': password,
        'exp': datetime.datetime.now()+datetime.timedelta(days=2)
    }
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token

def token_validation(username,password):

    data = {
        'username': username,
        'password': password,
    }
    token_data = requests.post(AUTH_ENDPOINT,data=data)
    token = token_data.json()['access']
    return token

