"""
应用配置文件
"""
import os
from pathlib import Path


class Config:
    """应用配置类"""
    
    # 项目根目录
    PROJECT_ROOT = Path(__file__).parent.parent
    
    # 数据目录
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    INTERIM_DATA_DIR = DATA_DIR / "interim"
    EXTERNAL_DATA_DIR = DATA_DIR / "external"
    
    # 输出目录
    OUTPUT_DIR = PROJECT_ROOT / "output"
    
    # 默认数据文件路径
    DEFAULT_HERB_FILE = PROCESSED_DATA_DIR / "herb.txt"
    
    # 默认输出文件路径
    DEFAULT_OUTPUT_FILE = OUTPUT_DIR / "herbs.csv"
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 解析器配置
    PARSER_PATTERN = r'[。$]\n^([\u4e00-\u9fa5 ]+)\s*([a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]+).*《([^》]+)》'
    
    # 默认提取的药材数量
    DEFAULT_N_HERBS = 5