from flask import jsonify
import jwt

def response(type, status, content, message=None):
    if type == 'create':
        if status == 'success':
            return success(content, 'Created', message)
        elif status == 'unauthorized':
            return unauthorized(content, 'Create', message)
        return failed(content, 'Create', message)


    elif type == 'retrieve':
        if status == 'success':
            return success(content, 'Retrieved', message)
        elif status == 'unauthorized':
            return unauthorized(content, 'Retrieve', message)
        return failed(content, 'Retrieve', message)

    elif type == 'update':
        if status == 'success':
            return success(content, 'Updated', message)
        elif status == 'unauthorized':
            return unauthorized(content, 'Update', message)
        return failed(content, 'Update', message)

    elif type == 'destroy':
        if status == 'success':
            return success(content, 'Deleted', message)
        elif status == 'unauthorized':
            return unauthorized(content, 'Delete', message)
        return failed(content, 'Delete', message)
    else:
        return failed(content, 'Proceed', message)


def success(content, msg, message=None):
    res = {}
    res['content'] = content
    resp = {}
    resp['status'] = 200
    resp['message'] = f'Successfully {msg}'
    if message:
        resp['message'] = message
    res['response'] = resp
    response = jsonify(res)
    response.status_code = 200
    response.content_type = "application/json"
    return response


def failed(content, msg, message=None):
    res = {}
    res['content'] = content
    resp = {}
    resp['status'] = 400
    resp['message'] = f'Failed to {msg}'
    if message:
        resp['message'] = message
    res['response'] = resp
    response = jsonify(res)
    response.status_code = 400
    response.content_type = "application/json"
    return response


def unauthorized(content, msg, message=None):
    res = {}
    res['content'] = content
    resp = {}
    resp['status'] = 401
    resp['message'] = f'Not Authorized to {msg}'
    if message:
        resp['message'] = message
    res['response'] = resp
    response = jsonify(res)
    response.status_code = 401
    response.content_type = "application/json"
    return response

def get_user_id(request):
    token = request.headers['x-access-token']
    if not token:
        return False,""
    print(token) 
    current_user = jwt.decode(token,algorithms=["HS256"],options={"verify_signature": False})
    print(current_user)

    return  True,current_user["userid"]
    