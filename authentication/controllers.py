from flask import Blueprint, request , url_for
from flask_mail import Message
from common.responses import  get_user_id

from flask import url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

s= URLSafeTimedSerializer('secretkey')

from authentication.views import signup_views, login_views, logout_views,get_reset_token,verify_reset_token

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
        subscribed = request.json['subscribed']
        userrequest=({"userid": userid,"firstname": firstname, "lastname" : lastname,"email":email,"password":password,"gender":gender,"dob":dob,"subscribed":subscribed})
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

    return "Email Verified"


@authentication.route('login', methods=['POST'])
def login_controller():
    if request.method == 'POST':
        return login_views(request.json['email'],request.json['password'])


@authentication.route('logout', methods=['POST'])
def logout_controller():
    return logout_views(request)





@authentication.route('forgotpassword', methods=['GET','POST'])
def forgotpassword():
    email = request.json['email']
    token = get_reset_token(email)
    print(token)
    msg = Message()
    msg.subject = "Password Reset"
    msg.sender = "praveena.mohandas@divum.in"
    msg.recipients = [email]
    link = url_for('authentication-api.reset_password',token=token,_external=True)
    msg.body='Your link is {}'.format(link)
    from app import mail
    mail.send(msg)
    # return verify_reset_token(token)
    return "verification link sent"


@authentication.route('reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    try:
        print("entere")
        return verify_reset_token(token)
    except SignatureExpired:
        return "Token Expired"












# @authentication.route('resetpassword', methods=['GET','POST'])
# def resetpassword():
#     email = request.json['email']
#     token = get_reset_token(email)
#     print(token)
#     msg = Message()
#     msg.subject = "Password Reset"
#     msg.sender = "praveena.mohandas@divum.in"
#     msg.recipients = [email]
#     link = url_for('authentication-api.confirm_password',token=token,_external=True)
#     msg.body='Your link is {}'.format(link)
#     from app import mail
#     mail.send(msg)
#     # return verify_reset_token(token)
#     return "verification link sent"

# # @authentication.route('resetpassword/<token>', methods=['GET','POST'])
# # def resetpassword(token):
# #     return verify_reset_token(token)

# @authentication.route('confirm_password/<token>', methods=['GET','POST'])
# def confirm_password(token):
#     try:
#         print("entere")
#         return verify_reset_token(token)
#     except SignatureExpired:
#         return "Token Expired"

