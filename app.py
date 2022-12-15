
from settings.build_app import create_app

app = create_app()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
db.init_app(app)

from dotenv import load_dotenv
load_dotenv()

# mail settings
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'praveenamk8@gmail.com'
app.config['MAIL_PASSWORD'] = '***'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

from flask_mail import Mail
mail = Mail(app)

import secrets
app.config['SECRET_KEY'] = secrets.token_urlsafe(12)
secretkey=app.config['SECRET_KEY']

if __name__ == "__main__":
    # print(app.url_map)
    app.run(host='localhost', port=5000, debug=True)
