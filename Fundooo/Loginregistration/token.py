
import datetime
import pdb
import jwt
import requests
from Fundooo.settings import SECRET_KEY

def token_activation(username, password):

    data = {
        'username': username,
        'password': password,
        'exp': datetime.datetime.now()+datetime.timedelta(days=2)
    }
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token


