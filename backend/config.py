# 日志等级
import os

CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
LOG_LEVEL = INFO

# 项目路劲
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库
DB_NAME = "AITP"
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/' + DB_NAME
