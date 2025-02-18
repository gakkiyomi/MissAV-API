
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    # 创建根日志器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 定义日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台处理器（开发环境）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # 文件处理器（生产环境）
    file_handler = RotatingFileHandler(
        filename='logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 错误日志专用处理器
    error_handler = RotatingFileHandler(
        filename='logs/error.log',
        maxBytes=5*1024*1024,
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    # 禁用第三方库的冗余日志
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
