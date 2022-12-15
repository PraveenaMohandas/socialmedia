from werkzeug.security import generate_password_hash, check_password_hash

from common.responses import response,unauthorized

from common.execute_raw_query import execute_query_without_return_value, fetch_records

from sqlalchemy import text

import jwt
from datetime import datetime,timedelta
from functools import wraps
from flask import session, jsonify, make_response

def signup_views(userrequest):
    try:
        userdata=userrequest
        query="insert into signup (first_name,last_name,email, password, gender, dob) values ('{first_name}','{last_name}','{email}','{password}','{gender}','{dob}');".format(first_name=userdata['firstname'],last_name=userdata['lastname'],
        email=userdata['email'],
        password=userdata['password'],
        gender=userdata['gender'],
        dob=userdata['dob'])
        execute_query_without_return_value(query)
        return response('create', 'success', {})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return response('create', 'success', {}, str(e))


def login_views(userrequest):
    try:
        from app import secretkey
        print(secretkey)
        logindata = userrequest
        email= logindata['email']
        query = "select email,password from signup where email='{email}';".format(email=email)
        dbdata=fetch_records(query)
        for i in range(len(dbdata)):
            useremail= dbdata[i]['email']
            password=dbdata[i]['password']

        if logindata['email'] == useremail and logindata['password'] == password:
            session['logged_in'] = True
            token = jwt.encode({
                'user':logindata['email'],
                'expiration':str(datetime.utcnow()+timedelta(seconds=120))
            },
            secretkey)

            return response('retrieve', 'success', token)
        else:
            return make_response('Unable to verify',403, {'WWW-Authenticate':'Basic realm:"Authentication Failed!'})
    except Exception as e:
        return response('retrieve', 'failed', {}, str(e))


def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        from flask import request
        from app import secretkey

        token=request.args.get('token')
        if not token:
            return jsonify({'Alert!':'Token is missing !'})
        try:
            payload = jwt.decode(token,secretkey)
            print(payload)
        except:
            return jsonify({'Alert!':'Invalid Token !'})
    return decorated


def logout_views(request):
    try:
        return response('create', 'success', {}, "Logout Successful")
    except Exception as e:
        return response('create', 'failed', {}, str(e))
