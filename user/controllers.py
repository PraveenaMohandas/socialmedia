from flask import Blueprint
from flask import json,jsonify
from io import StringIO
import csv
from .views import getuserdata,updateuserdata,friendslist
from werkzeug.wrappers import Response

user = Blueprint('profile-api', __name__, url_prefix='/api/v1/user/')
from flask import request

from common.responses import response, get_user_id
from common.execute_raw_query import execute_query_without_return_value, fetch_records


from decouple import config
db_connection = 'postgresql://{}:{}@{}:{}/{}'.format(
config('user'),
config('password'),
config('host'),
config('port'),
config('db_name')
)
from sqlalchemy import create_engine
engine= create_engine(db_connection)
import pandas as pd


@user.route('profile', methods=['GET','POST'])
def auth():
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

@user.route('getallusers', methods=['GET','POST'])
def getallusers():
    status,userid=get_user_id(request)
    if not status:
        return response('create', 'unauthorized',{"Token is missing"})
    try:
        query = "select * from users where not userid='{userid}';".format(userid=userid)
        usersdata=fetch_records(query)
        return response('retrieve', 'success',usersdata   )

    except Exception as e:
        return response('failed', 'failed', {}, str(e))

@user.route('sendrequest/<receiverid>', methods=['GET','POST'])
def sendreq(receiverid):
    status,userid=get_user_id(request)
    if not status:
        return response('create', 'unauthorized',{"Token is missing"})
    selectquery ="select receiverid from friends where userid='{userid}';".format(userid=userid)
    requestdata=fetch_records(selectquery)
    if not any(d['receiverid'] == receiverid for d in requestdata):
        query="insert into friends (userid,receiverid,status) values ('{userid}','{receiverid}','{status}') ;".format(userid=userid,receiverid=receiverid,status="pending")
        friendslistdata=execute_query_without_return_value(query)
        # friendslist to mongodb
        friendslist()
    else:
        return response('create', 'failed',"Request Already Sent")
 

    return response('create', 'success', "Request Sent")

@user.route('followreqlist', methods=['GET','POST'])
def reqlist():
    status,userid=get_user_id(request)
    try:
        query = "select * from friends where receiverid ='{userid}';".format(userid=userid)
        reqlist=fetch_records(query)
        return response('retrieve', 'success',reqlist)

    except Exception as e:
        return response('failed', 'failed', {}, str(e))

@user.route('acceptrequest', methods=['GET','POST'])
def acceptreq():
    requestlist = request.json['requestlist']
    for i in range(len(requestlist)):
        userid = requestlist[i]['userid']
        statusquery="update friends  set status='Accepted' where userid ='{userid}';".format(userid=userid)
        statusupdate = execute_query_without_return_value(statusquery)
        return response('update', 'success',"Request Accepted")

@user.route('save/<postid>', methods=['GET','POST'])
def savefeed(postid):
    status,userid=get_user_id(request)
    userfeed = request.json['userfeed']
    try:
        query="insert into userfeed (userid,postid,title,description,image,tags,category,visibility,deleted_at) values ('{userid}','{postid}','{title}','{description}','{image}','{tags}','{category}','{visibility}',NULL);".format(userid=userid,postid=postid,title=userfeed['title'],description=userfeed['description'],image=userfeed['image'],tags=userfeed['tags'],category=userfeed['category'],visibility=userfeed['visibility'])
        execute_query_without_return_value(query)
        return response('create', 'success', "User feed Saved")
    except Exception as e:
        return response('failed', 'failed', {}, str(e))

@user.route('getuserfeed', methods=['GET','POST'])
def getfeed():
    visibility = request.json['visibility']
    from app import cache
    cacheduserfeed = cache.get("userfeed")
    if cacheduserfeed:
        return response('retrieve', 'success',cacheduserfeed)
    else:
        query = "select * from userfeed where visibility ='{visibility}' and deleted_at IS NULL;".format(visibility=visibility)
        getuserfeed=fetch_records(query)
        # caching using redis
        cache.set("userfeed", json.dumps(getuserfeed))
        return response('retrieve', 'success',getuserfeed)
   
@user.route('deleteuserfeed/<postid>', methods=['GET','POST'])
def deletefeed(postid):
    status,userid=get_user_id(request)
    deletequery = "UPDATE userfeed SET deleted_at = now() WHERE userid='{userid}' and postid ='{postid}';".format(postid=postid,userid=userid)
    deleteuserfeed = execute_query_without_return_value(deletequery)
    return response('update', 'success',"deleted")


@user.route('download/csv', methods=['GET', 'POST'])
def generate_csv():
    try:
        dataFrame = pd.read_sql("select * from \"userfeed\"", engine )

        file = dataFrame.to_csv(index=False, lineterminator="\n")
        return Response(
        file,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=sample.csv"})
        
    except Exception as e:
        return response('failed', 'failed', {}, str(e))


@user.route('getcsvdata', methods=['GET','POST'])
def getcsvdata():
    df = pd.read_csv('userfeed.csv')
    try:
        df.to_sql('userfeed', engine, if_exists= 'replace')
        return response('create', 'success',"Saved")
    except Exception as e:
        return response('failed', 'failed', {}, str(e))

