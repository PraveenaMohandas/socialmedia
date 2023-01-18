
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
app.config['MAIL_USERNAME'] = 'praveena.mohandas@divum.in'
app.config['MAIL_PASSWORD'] = 'Praveena@divum'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


#  MongoDB Integration 
import pymongo

connection_url = "mongodb://localhost:27017/"
client=pymongo.MongoClient(connection_url)
database_name="socialmedia"
socialmedia_db=client[database_name]
collection_name="friends"
collection=socialmedia_db[collection_name]

# socialmedia_db.list_collection_names()
# client.list_database_names()


# Redis Implementation 
import redis
cache = redis.Redis(host='localhost',port='6379',db=0)

from flask_mail import Mail
mail = Mail(app)

import secrets
app.config['SECRET_KEY'] = secrets.token_urlsafe(12)
SECRET_KEY=app.config['SECRET_KEY']

from apscheduler.schedulers.background import BackgroundScheduler
# import atexit
from flask_mail import Message

def sendnewsletter():
    with app.app_context():
        from common.execute_raw_query import fetch_records
        query = "select email from users where subscribed is TRUE;"
        dbdata=fetch_records(query)
        for i in range(len(dbdata)):
            email=dbdata[i]['email']
            print(email)
            msg = Message('Newsletter', sender="praveena.mohandas@divum.in",recipients=[email])
            msg.body='News Today'
            mail.send(msg)

scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
scheduler.add_job(func=sendnewsletter, trigger='cron',day='*',hour='10')
# scheduler.add_job(func=sendnewsletter, trigger='cron',second='10')

scheduler.start()

# atexit.register(lambda: scheduler.shutdown())



# from flask_crontab import Crontab
# crontab = Crontab(app)
# from user.controllers import do_something
# @crontab.job(minute="1")
# def my_scheduled_job():
#     print("fun")
#     do_something()


if __name__ == "__main__":
    # print(app.url_map)
    app.run(host='localhost', port=5000, debug=True)

