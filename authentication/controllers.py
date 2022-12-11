from flask import Blueprint, request 

from authentication.views import signup_views, login_views, logout_views

authentication = Blueprint('authentication-api', __name__, url_prefix='/api/v1/authentication/')

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
    email = "ajay@gmail.com"
    password = "pwd"
    gender = "male"
    dob = "19-2-1999"
    
    request=({"firstname": firstname, "lastname" : lastname,"email":email,"password":password,"gender":gender,"dob":dob})


    return signup_views(request)


@authentication.route('login', methods=['POST'])
def login_controller():
    # email = request.form['email']
    # password = request.form['password']
    email = "ajay@gmail.com"
    password = "pwd"
    request=({"email":email,"password":password})
    return login_views(request)


@authentication.route('logout', methods=['POST'])
def logout_controller():
    return logout_views(request)
