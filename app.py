
from settings.build_app import create_app

app = create_app()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
db.init_app(app)

from dotenv import load_dotenv
load_dotenv()

from flask_mail import Mail#issue
mail = Mail(app)#issue

if __name__ == "__main__":
    # print(app.url_map)
    app.run(host='localhost', port=5000, debug=True)
