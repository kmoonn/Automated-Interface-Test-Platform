import os

# 日志等级
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
LOG_LEVEL = INFO

# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库连接配置
USER_NAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = 3306
DB_NAME = "AITP"
