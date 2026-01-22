#!/usr/bin/env python3
"""
TCM-HerbDB 命令行入口点
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tcm_herbdb.cli import main

if __name__ == "__main__":
    main()