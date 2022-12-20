from flask import Blueprint
from flask import jsonify

from .views import getuserdata,updateuserdata

user = Blueprint('profile-api', __name__, url_prefix='/api/v1/user/')
from flask import request

from common.responses import response, get_user_id


@user.route('profile', methods=['GET','POST'])
def auth():
    print("yesss")
    status,userid=get_user_id(request)
    if not status:
        return response('create', 'unauthorized',{"Token is missing"})
   
    return getuserdata(userid)

@user.route('updateprofile', methods=['GET','POST'])
def updatedata():
    updateddata = request.json['updateddata']
    status,userid=get_user_id(request)
    updatedata= ({"firstname": updateddata['firstname'], "lastname" : updateddata['lastname'],"email":updateddata['email'],"gender":updateddata['gender'],"dob":updateddata['dob']})
    if not status:
        return response('create', 'unauthorized',{"Token is missing"})
    return updateuserdata(updatedata,userid)



