import datetime
from flask import Flask
from .models.base import setup_db
from .apis.place_routes import place_app
from .apis.user_routes import user_app
from .apis.comment_routes import comment_app
from .apis.like_routes import like_app
import logging

app = Flask(__name__)
setup_db(app)
logging.basicConfig(filename='logs/{}.log'.format(datetime.date.today().strftime('%Y-%m-%d')), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.register_blueprint(user_app)
app.register_blueprint(place_app)
app.register_blueprint(comment_app)
app.register_blueprint(like_app)

