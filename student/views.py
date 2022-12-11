from common.execute_raw_query import fetch_records
from common.responses import response

# https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
def student_operations(request, id=None):
    try:
        if request.method == 'POST':

            return response('create', 'success', {})
        elif request.method == 'GET':
            if id:
                return response('retrieve', 'success', {})
            query = "select * from cms_users"
            result = fetch_records(query)
            return response('retrieve', 'success', {"data": result})

        elif request.method == 'PUT':
            if not id:
                return response('update', 'failed', {})

            return response('update', 'success', {})

        elif request.method == 'DELETE':
            if not id:
                return response('update', 'failed', {})
            return response('destroy', 'success', {})

    except Exception as e:
        return response('failed', 'failed', {}, str(e))
