from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from backend.config import USER_NAME, PASSWORD, HOST, PORT, DB_NAME
from backend.utils.logging_utils import init_logging

# 初始化日志器
init_logging()

# 初始化Flask对象
app = Flask(__name__)

# 配置数据库连接
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# 配置密钥
app.config['SECRET_KEY'] = "hushan0223"

# 创建SQLAlchemy对象
db = SQLAlchemy(app)

# 创建flask restful对象
api = Api(app)

# 初始化登录
login_manager = LoginManager()
login_manager.init_app(app)

