from flask import jsonify


def homepage(app):
    @app.route("/", methods=['GET'])
    def home_page():
        return "<h4 style='text-align:center'>STUDENT APP</h4>"


def global_errorhandler(app):
    @app.errorhandler(Exception)
    def return_error(e):
        res = dict()
        res["content"] = {'err': 'Internal Error', 'err_msg': str(e)}
        res["response"] = {}
        res["status"] = 500
        res["message"] = "Invalid request,please try again"
        response = jsonify(res)
        response.status_code = 500
        response.content_type = "application/json"
        return response
