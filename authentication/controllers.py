from flask import Blueprint, request , url_for
from flask_mail import Message


from itsdangerous import URLSafeTimedSerializer, SignatureExpired


from authentication.views import signup_views, login_views, logout_views

authentication = Blueprint('authentication-api', __name__, url_prefix='/api/v1/authentication/')


s= URLSafeTimedSerializer('secretkey')

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# mail accounts
MAIL_DEFAULT_SENDER = 'praveena.mohandas@gmail.com'

@authentication.route('signup', methods=['POST'])
def signup_controller():
    print("signup entered")
    request=""
    # firstname = request.form['firstname']
    # lastname = request.form['lastname']
    # email = request.form['email']
    # password = request.form['password']
    # gender = request.form['gender']
    # dob = request.form['dob']

    firstname = "AK"
    lastname = "Ajay"
    email = "xobev51046@fanneat.com"
    password = "pwd"
    gender = "male"
    dob = "19-2-1999"
        
    request=({"firstname": firstname, "lastname" : lastname,"email":email,"password":password,"gender":gender,"dob":dob})

    token = s.dumps(email,salt='email-confirm')
    print(token)

    msg = Message('Confirm Email', sender=[MAIL_DEFAULT_SENDER],recipients=[email])
    link = url_for('authentication-api.confirm_email',token=token,_external=True)
    msg.body='Your link is {}'.format(link)

    from app import mail
    mail.send(msg)


    return signup_views(request)

@authentication.route('confirm_email/<token>', methods=['GET','POST'])
def confirm_email(token):
    try:
        print("try")
        email=s.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        return "Token Expired"

    return "token works"


@authentication.route('login', methods=['POST'])
def login_controller():
    # email = request.form['email']
    # password = request.form['password']
    email = "xobev51046@fanneat.com"
    password = "pwd"
    request=({"email":email,"password":password})
    return login_views(request)


@authentication.route('logout', methods=['POST'])
def logout_controller():
    return logout_views(request)
