import logging

from flask import Flask
from backend.utils.logging_utils import init_logging

# 初始化日志器
init_logging()
logging.info("Test Logging")

app = Flask(__name__)

if __name__ == '__main__':
    app.run()
