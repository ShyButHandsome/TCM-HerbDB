"""
TCM-HerbDB 项目的日志配置模块
提供统一的日志配置和管理功能
"""
import logging
import sys
import os
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_file: str = None,
    log_format: str = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """
    设置项目的统一日志配置
    
    Args:
        level: 日志级别，默认为INFO
        log_file: 日志文件路径，如果为None则只输出到控制台
        log_format: 日志格式，如果为None则使用默认格式
        max_bytes: 单个日志文件最大大小（字节）
        backup_count: 保留的备份日志文件数量
    """
    # 如果没有指定日志格式，则使用默认格式
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 创建格式器
    formatter = logging.Formatter(log_format)
    
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # 清除现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 如果指定了日志文件，则添加文件处理器
    if log_file:
        # 确保日志目录存在
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建文件处理器（使用RotatingFileHandler支持日志轮转）
        try:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=max_bytes, 
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except ImportError:
            # 如果不支持RotatingFileHandler，则使用普通FileHandler
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
    
    # 配置tcm_herbdb包的日志记录器
    tcm_logger = logging.getLogger('tcm_herbdb')
    tcm_logger.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    return logging.getLogger(name)


# 默认配置
def configure_default_logging() -> None:
    """
    使用默认配置设置日志
    """
    log_file = os.getenv('TCM_HERBDB_LOG_FILE', 'logs/tcm_herbdb.log')
    log_level_str = os.getenv('TCM_HERBDB_LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    setup_logging(
        level=log_level,
        log_file=log_file
    )


# 如果模块被直接运行，则执行默认配置
if __name__ == '__main__':
    configure_default_logging()
    logger = get_logger(__name__)
    logger.info("日志模块测试")