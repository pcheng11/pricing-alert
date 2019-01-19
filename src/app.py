from src.common.database import Database


__author__ = 'victor cheng'

from flask import Flask, render_template

app = Flask(__name__)
# import config from config.py
app.config.from_object('config')
app.secret_key='123'

@app.before_first_request
def init_db():
    Database.initialize()

@app.route("/")
def home():
    return render_template("home.html")

from src.models.users.view import user_blueprint
from src.models.alerts.view import alert_blueprint
from src.models.stores.view import store_blueprint

app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(store_blueprint, url_prefix='/stores')

app.run(debug=app.config, port=5005)
