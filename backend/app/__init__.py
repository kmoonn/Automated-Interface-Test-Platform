from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from backend.config import USER_NAME, PASSWORD, HOST, PORT, DB_NAME
from backend.utils.logging_utils import init_logging

init_logging()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

api = Api(app)

