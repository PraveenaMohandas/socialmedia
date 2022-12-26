from flask import Blueprint
from flask import jsonify

from .views import getuserdata,updateuserdata

user = Blueprint('profile-api', __name__, url_prefix='/api/v1/user/')
from flask import request

from common.responses import response, get_user_id
from common.execute_raw_query import execute_query_without_return_value, fetch_records

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
        query = "select * from signup where not userid='{userid}';".format(userid=userid)
        usersdata=fetch_records(query)
        print(usersdata)
        return response('retrieve', 'success',usersdata   )

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return response('failed', 'failed', {}, str(e))

@user.route('sendrequest/<receiverid>', methods=['GET','POST'])
def sendreq(receiverid):
    status,userid=get_user_id(request)
    if not status:
        return response('create', 'unauthorized',{"Token is missing"})
    query="insert into friends (userid,receiverid,status) values ('{userid}','{receiverid}','{status}');".format(userid=userid,receiverid=receiverid,status="pending")
    execute_query_without_return_value(query)
    return response('create', 'success', "Request Sent")

@user.route('followreqlist', methods=['GET','POST'])
def reqlist():
    status,userid=get_user_id(request)
    try:
        query = "select * from friends where receiverid ='{userid}';".format(userid=userid)
        reqlist=fetch_records(query)
        print(reqlist)
        return response('retrieve', 'success',reqlist)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return response('failed', 'failed', {}, str(e))

@user.route('acceptrequest', methods=['GET','POST'])
def acceptreq():
    requestlist = request.json['requestlist']
    for i in range(len(requestlist)):
        userid = requestlist[i]['userid']
        statusquery="update friends  set status='Accepted' where userid ='{userid}';".format(userid=userid)
        statusupdate = execute_query_without_return_value(statusquery)
        return response('update', 'success',"Request Accepted")

@user.route('save', methods=['GET','POST'])
def savefeed():
    status,userid=get_user_id(request)
    userfeed = request.json['userfeed']
    print(userfeed) 
    try:
        image = userfeed[i]['image']
        from PIL import Image
        img = Image.open(image)
        print(img)
        for i in range(len(userfeed)):
            query="insert into userfeed (userid,title,description,image,tags,category,visibility,deleted_at) values ('{userid}','{title}','{description}','{image}','{tags}','{category}','{visibility}','{deleted_at}');".format(userid=userid,title=userfeed[i]['title'],description=userfeed[i]['description'],image=img,tags=userfeed[i]['tags'],category=userfeed[i]['category'],visibility=userfeed[i]['visibility'])
            execute_query_without_return_value(query)
            return response('create', 'success', "User feed Saved")
    except Exception as e:
            import traceback
            print(traceback.format_exc())
            return response('failed', 'failed', {}, str(e))

@user.route('getuserfeed', methods=['GET','POST'])
def getfeed():
    visibility = request.json['visibility']
    try:        
        query = "select * from userfeed where visibility ='{visibility}' and deleted_at IS NULL;".format(visibility=visibility)
        getuserfeed=fetch_records(query)
        print(getuserfeed)
        return response('retrieve', 'success',getuserfeed)
        
    except Exception as e:
        import traceback
        return response('failed', 'failed', {}, str(e))

@user.route('deleteuserfeed/<userid>', methods=['GET','POST'])
def deletefeed(userid):
    deletequery = "UPDATE users SET deleted_at = now() WHERE userid ='{userid}';".format(userid=userid)
    deleteuserfeed = execute_query_without_return_value(deletequery)
    print(deleteuserfeed)
    return response('update', 'success',"deleted")


# UPDATE users SET deleted_at = current_timestamp WHERE id = userid ='{userid}';".format(userid=userid)