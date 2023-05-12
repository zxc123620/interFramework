import datetime
import logging
import logging.handlers

# 初始化日志对象
logger = logging.getLogger('main')
logger.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

# 初始化日志文件对象
handler = logging.handlers.TimedRotatingFileHandler(filename="./log/" + str(datetime.date.today()) + ".log", when="D", interval=1,
                                                    backupCount=10, encoding="utf-8")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

# 初始化控制台对象
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

# 添加日志文件和控制台对象
logger.addHandler(handler)
logger.addHandler(console)