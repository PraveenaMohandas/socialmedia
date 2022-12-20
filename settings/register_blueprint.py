from authentication.controllers import authentication
from student.controllers import students
from user.controllers import user


def register_blueprint(app):
    app.register_blueprint(students)
    app.register_blueprint(authentication)
    app.register_blueprint(user)

    return app
