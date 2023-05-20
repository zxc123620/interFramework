import datetime
import logging
import logging.handlers

# 获取项目根路径
from config import ROOT_PATH

# 初始化日志对象
logger = logging.getLogger('main')
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

# 初始化日志文件对象
handler = logging.handlers.TimedRotatingFileHandler(filename=f"{ROOT_PATH}/log/" + str(datetime.date.today()) + ".log", when="D",
                                                    interval=1,
                                                    backupCount=10, encoding="utf-8")
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

# 初始化控制台对象
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

# 添加日志文件和控制台对象
logger.addHandler(handler)
logger.addHandler(console)

