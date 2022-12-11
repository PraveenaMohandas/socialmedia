from authentication.controllers import authentication
from student.controllers import students


def register_blueprint(app):
    app.register_blueprint(students)
    app.register_blueprint(authentication)
    return app
