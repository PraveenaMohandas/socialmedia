from werkzeug.security import generate_password_hash, check_password_hash

from common.responses import response,unauthorized

from common.execute_raw_query import execute_query_without_return_value, fetch_records

import jwt
from datetime import datetime,timedelta
from flask import session, jsonify, make_response

def signup_views(userrequest):
    try:
        userdata=userrequest
        query="insert into users (userid,first_name,last_name,email, password, gender, dob,subscribed) values ('{userid}','{first_name}','{last_name}','{email}','{password}','{gender}','{dob}','{subscribed}');".format(userid=userdata['userid'],first_name=userdata['firstname'],last_name=userdata['lastname'],
        email=userdata['email'],
        password=userdata['password'],
        gender=userdata['gender'],
        dob=userdata['dob'],subscribed=userdata['subscribed'])
        execute_query_without_return_value(query)
        return response('create', 'success', {})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return response('create', 'success', {}, str(e))


def login_views(email,password):
    try:
        from app import SECRET_KEY
        print(SECRET_KEY)
        query = "select userid,password from users where email='{email}';".format(email=email)
        dbdata=fetch_records(query)
        print(dbdata)
        for i in range(len(dbdata)):
            userid=dbdata[i]['userid']
            userpassword=dbdata[i]['password']

        if email and password == userpassword:
            session['logged_in'] = True
            dt=datetime.now()+timedelta(minutes=15)
            exp=dt.strftime("%H:%M:%S")
            token = jwt.encode({
                'userid':userid,
                'user':email,
                'expiration':str(exp)
            },
            SECRET_KEY)

            return response('retrieve', 'success', token)
        else:
            return make_response('Unable to verify',403, {'WWW-Authenticate':'Basic realm:"Authentication Failed!'})
    except Exception as e:
        return response('retrieve', 'failed', {}, str(e))

def logout_views(request):
    try:
        return response('create', 'success', {}, "Logout Successful")
    except Exception as e:
        return response('create', 'failed', {}, str(e))


def get_reset_token(email):
    import uuid
    reset_token = uuid.uuid4()
    from datetime import datetime, timezone

    dt = datetime.now(timezone.utc)
    query="insert into resetpassword (email,reset_token,requested_on) values ('{email}','{reset_token}','{requested_on}');".format(reset_token=reset_token,email=email,requested_on=dt)
    execute_query_without_return_value(query)
    return reset_token

def verify_reset_token(token):
    try:
        print(token)
        query = "select email,reset_token from resetpassword where reset_token='{reset_token}';".format(reset_token=token)
        dbdata=fetch_records(query)
        return response('create', 'success', {}, "Reset Successful")
    except Exception as e:
        return response('create', 'failed', {}, str(e))

