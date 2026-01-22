#!/usr/bin/env python3
"""
TCM-HerbDB 项目演示脚本

此脚本演示了如何使用 TCM-HerbDB 项目提取和分析中药数据
"""
import os
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from tcm_herbdb.herb_parser import extract_herb_info
from tcm_herbdb.database import HerbDatabase


def main():
    print("TCM-HerbDB 项目演示")
    print("=" * 50)

    # 检查数据文件是否存在
    data_file = Path(__file__).parent / "data" / "processed" / "herb.txt"
    if not data_file.exists():
        print(f"错误: 找不到数据文件 {data_file}")
        return

    print(f"正在读取数据文件: {data_file}")

    # 读取并解析药材数据
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("正在解析药材信息...")
    herbs = extract_herb_info(content)

    print(f"成功提取了 {len(herbs)} 味药材的信息")
    print()

    # 显示前5味药材的详细信息
    print("前5味药材的详细信息:")
    print("-" * 50)
    for i, herb in enumerate(herbs[:5]):
        print(f"{i+1}. 药材名: {herb['name']}")
        print(f"   拼音: {herb['pinyin']}")
        print(f"   来源: {herb['source']}")
        print(f"   药性: {herb['properties'][:50]}...")
        print(f"   功效: {herb['efficacy'][:50]}...")
        print(f"   应用: {herb['application'][:50]}...")
        print()

    # 统计信息
    print("统计信息:")
    print("-" * 50)
    print(f"总药材数: {len(herbs)}")

    # 计算有多少味药材有完整的药性信息
    herbs_with_properties = sum(1 for herb in herbs if herb['properties'])
    print(f"有药性信息的药材数: {herbs_with_properties}")

    # 计算有多少味药材有完整的功效信息
    herbs_with_efficacy = sum(1 for herb in herbs if herb['efficacy'])
    print(f"有功效信息的药材数: {herbs_with_efficacy}")

    # 计算有多少味药材有完整的应用信息
    herbs_with_application = sum(1 for herb in herbs if herb['application'])
    print(f"有应用信息的药材数: {herbs_with_application}")

    # 创建数据库实例并导出到CSV
    print("\n正在生成CSV文件...")
    db = HerbDatabase(herbs)

    # 确保输出目录存在
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # 导出到CSV
    csv_file = output_dir / "herbs.csv"
    db.export_to_csv(str(csv_file))

    print(f"CSV文件已生成: {csv_file}")
    print(f"CSV文件大小: {csv_file.stat().st_size} 字节")

    print()
    print("演示完成！")
    print("完整数据已保存到 output/herbs.csv 文件")


if __name__ == "__main__":
    main()