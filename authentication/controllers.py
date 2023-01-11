from flask import Blueprint, request , url_for
from flask_mail import Message
 

from flask import url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

s= URLSafeTimedSerializer('secretkey')

from authentication.views import signup_views, login_views, logout_views

authentication = Blueprint('authentication-api', __name__, url_prefix='/api/v1/authentication/')


@authentication.route('signup', methods=['GET','POST'])
def signup_controller():
    if request.method == 'POST':
        userid =request.json['userid']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        email = request.json['email']
        password = request.json['password']
        gender = request.json['gender']
        dob = request.json['dob']
        
        userrequest=({"userid": userid,"firstname": firstname, "lastname" : lastname,"email":email,"password":password,"gender":gender,"dob":dob})
        token = s.dumps(email,salt='email-confirm')
        msg = Message('Confirm Email', sender="praveena.mohandas@divum.in",recipients=[email])
        link = url_for('authentication-api.confirm_email',token=token,_external=True)
        msg.body='Your link is {}'.format(link)
        from app import mail
        mail.send(msg)


        return signup_views(userrequest)

@authentication.route('confirm_email/<token>', methods=['GET','POST'])
def confirm_email(token):
    try:
        email=s.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        return "Token Expired"

    return "token works"


@authentication.route('login', methods=['POST'])
def login_controller():
    if request.method == 'POST':
        return login_views(request.json['email'],request.json['password'])


@authentication.route('logout', methods=['POST'])
def logout_controller():
    return logout_views(request)


