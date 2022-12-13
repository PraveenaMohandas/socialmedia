from werkzeug.security import generate_password_hash, check_password_hash

from common.responses import response

from common.execute_raw_query import execute_query_without_return_value

from sqlalchemy import text

def signup_views(request):
    try:
        userdata=request

        # # db.execute("Select * from signup WHERE first_name=%s",(userdata["firstname"]))
        # pwdhash= generate_password_hash(password=userdata["password"])
        # userdata["password"]= 'wdfjejrf'
        # print(pwdhash)

        # columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in userdata.keys())
        # values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in userdata.values())
        # query = text("INSERT INTO %s ( %s ) VALUES ( %s );" % ('public.signup', columns, values))
        
        # query = text('INSERT INTO "signup" ("first_name","last_name","email","password","gender","dob") VALUES (:firstname, :lastname,:email,:password,:gender,dob)')
        

        query="insert into signup (first_name,last_name,email, password, gender, dob) values ('{first_name}','{last_name}','{email}','{password}','{gender}','{dob}');".format(first_name=userdata['firstname'],last_name=userdata['lastname'],
        email=userdata['email'],
        password=userdata['password'],
        gender=userdata['gender'],
    dob=userdata['dob'])
        # query = text('INSERT INTO employee ("first_name","first_name","email","password","gender","dob") VALUES (userdata["firstname"], userdata["lastname"],userdata["email"],pwdhash,userdata["gender"],userdata["dob"])')
        execute_query_without_return_value(query)
        return response('create', 'success', {})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return response('create', 'success', {}, str(e))


def login_views(request):
    try:
        logindata = request
        # pwdhash = "select password from signup where email=logindata["email"]"
        pwdhash ="pbkdf2:sha256:260000$84j9HEgp6H2pRO3v$d6509934c04eeaae6af81463e2f331aa9245869233e999841e90196e2395fd5f"
        if not check_password_hash(pwhash=pwdhash, password=logindata["password"]):
            return response('retrieve', 'unauthorized', {}, 'Invalid Password')
        return response('retrieve', 'success', {})
    except Exception as e:
        return response('retrieve', 'failed', {}, str(e))


def logout_views(request):
    try:
        return response('create', 'success', {}, "Logout Successful")
    except Exception as e:
        return response('create', 'failed', {}, str(e))
