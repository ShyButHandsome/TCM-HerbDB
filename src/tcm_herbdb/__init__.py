from .logging_config import setup_logging, get_logger, configure_default_logging

# 导入config模块
from .config import Config

# 导入herb_parser模块中的函数和类
from .herb_parser import (
    HerbParser,
    HerbDatabase as BaseHerbDatabase,
    extract_herb_info,
    extract_section,
    get_first_n_herbs,
    extract_herb_info_from_txt,
    get_first_n_herbs_from_txt
)

# 导入database模块中的扩展类
from .database import HerbDatabase as ExtendedHerbDatabase, BaseHerbDatabase

# 导入cli模块
from .cli import main as cli_main

# 定义包的公共接口
__all__ = [
    # 日志相关
    'setup_logging',
    'get_logger',
    'configure_default_logging',

    # 配置相关
    'Config',

    # 解析器相关
    'HerbParser',
    'HerbDatabase',
    'BaseHerbDatabase',
    'ExtendedHerbDatabase',
    'extract_herb_info',
    'extract_section',
    'get_first_n_herbs',
    'extract_herb_info_from_txt',
    'get_first_n_herbs_from_txt',

    # CLI相关
    'cli_main'
]

# 为向后兼容性保留HerbDatabase
HerbDatabase = ExtendedHerbDatabase


def hello() -> str:
    """
    简单的问候函数
    """
    logger = get_logger(__name__)
    logger.info("Hello from tcm-herbdb!")
    return "Hello from tcm-herbdb!"
