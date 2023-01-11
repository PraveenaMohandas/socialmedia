from common.execute_raw_query import execute_query_without_return_value, fetch_records
from common.responses import response

def getuserdata(userid):
    try:
        query = "select * from users where userid='{userid}';".format(userid=userid)
        userprofiledata=fetch_records(query)
        print(userprofiledata)
        return response('retrieve','success',userprofiledata)

    except Exception as e:
        return response('failed', 'failed', {}, str(e))


def updateuserdata(updatedata,userid):
    try:
        updatequery="update users  set first_name='{first_name}',last_name='{last_name}',email='{email}',gender='{gender}',dob='{dob}' where userid ='{userid}';".format(first_name=updatedata['firstname'],last_name=updatedata['lastname'],email=updatedata['email'],gender=updatedata['gender'],dob=updatedata['dob'],userid=userid)
        updateduserdata = execute_query_without_return_value(updatequery)
        print(updateduserdata)
        return response('update', 'success',"Updated")

    except Exception as e:
        return response('failed', 'failed', {}, str(e))


def friendslist():
    try:
        from app import collection
        mongoquery ="select * from friends"
        friendslist=fetch_records(mongoquery)
        print("----",friendslist)
        for i in range(len(friendslist)):
            print("====",friendslist[i])
        collection.insert_many(friendslist)
        
        # collection.update_many({},upsert=True)
    except Exception as e:
        return response('failed', 'failed', {}, str(e))
    