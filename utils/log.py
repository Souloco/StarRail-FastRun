from loguru import logger
import os
# 根路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# log路径
log_dir = os.path.join(root_dir,"logs")
log_path = os.path.join(log_dir,'日志文件.log')

log = logger.bind(file=log_path)
log.add(log_path,format="{time:HH:mm:ss} " + "|{level}| " + "{module}.{function}:{line} - {message}",
        rotation="1 days",enqueue=True,serialize=False,encoding="utf-8",retention="14 days")
