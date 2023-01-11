from base64 import b64decode
from flask import request, jsonify
from functools import wraps
from common.responses import response
import jwt
from datetime import datetime,timedelta


def middleware(app):
    @app.before_request
    def process_request():
        try:
            # request.endpoint,request.url,request.path
            api = ((request.path).split('?')[0]).split('/')
            print(api)

            if 'authentication' in api:
                pass
            elif 'csv' in api:
                pass
            elif 'user' in api:
                status=token_required(request)
                print(status)
                if not status:
                    return response('create', 'unauthorized', {})
                   
            else:
                return response('create', 'unauthorized', {})
        except Exception as e:
            print(e)
            return response('create', 'unauthorized', {}, str(e))

def token_required(request):
    token=None
    token = request.headers['x-access-token']
    if not token:
        return False
    print(token) 
    
    current_user = jwt.decode(token,algorithms=["HS256"],options={"verify_signature": False})
    print(current_user)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if current_time > current_user['expiration']:
        print("yes time expired ")
        return False    

    return True

def validate_auth_token(token):
    try:
        return 1
    except Exception as e:
        return -1
