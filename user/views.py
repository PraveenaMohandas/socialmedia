from common.execute_raw_query import execute_query_without_return_value, fetch_records
from common.responses import response

def getuserdata(userid):
    try:
        query = "select * from signup where userid='{userid}';".format(userid=userid)
        userprofiledata=fetch_records(query)
        print(userprofiledata)
        return response('retrieve', 'success',userprofiledata   )

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return response('failed', 'failed', {}, str(e))


def updateuserdata(updatedata,userid):
    try:
        updatequery="update signup  set first_name='{first_name}',last_name='{last_name}',email='{email}',gender='{gender}',dob='{dob}' where userid ='{userid}';".format(first_name=updatedata['firstname'],last_name=updatedata['lastname'],email=updatedata['email'],gender=updatedata['gender'],dob=updatedata['dob'],userid=userid)
        updateduserdata = execute_query_without_return_value(updatequery)
        print(updateduserdata)
        return response('update', 'success',"Updated")

    except Exception as e:
        return response('failed', 'failed', {}, str(e))