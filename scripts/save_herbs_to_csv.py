#!/usr/bin/env python3
"""
将药材信息保存到CSV文件的脚本
"""
import os
import sys
from pathlib import Path

# 由于项目已安装为可编辑包，可以直接导入
from tcm_herbdb import ExtendedHerbDatabase


def main():
    print("正在将药材信息保存到CSV文件...")

    # 检查数据文件是否存在
    # 从脚本文件向上两级目录找到项目根目录
    project_root = Path(__file__).parent.parent
    data_file = project_root / "data" / "processed" / "herb.txt"
    if not data_file.exists():
        print(f"错误: 找不到数据文件 {data_file}")
        return

    print(f"正在从 {data_file} 加载药材数据...")

    # 从txt文件创建数据库实例
    db = ExtendedHerbDatabase.from_txt_file(str(data_file))

    print(f"成功加载了 {db.get_herb_count()} 味药材的信息")

    # 确保输出目录存在
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)

    # 导出到CSV
    csv_file = output_dir / "herbs.csv"
    db.export_to_csv(str(csv_file))

    print(f"药材信息已成功保存到 {csv_file}")
    print(f"CSV文件大小: {csv_file.stat().st_size} 字节")


if __name__ == "__main__":
    main()