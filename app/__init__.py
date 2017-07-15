from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path='/static')
app.config.from_object("config")

from app.ws.controllers import ws

app.register_blueprint(ws)

# db variable initialization
#db = SQLAlchemy()
