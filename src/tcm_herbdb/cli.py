"""
命令行接口模块
"""
import argparse
import sys
from pathlib import Path

# 使用当前工作目录作为项目根目录
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

from tcm_herbdb.herb_parser import HerbParser
from tcm_herbdb.database import HerbDatabase as ExtendedHerbDatabase
from tcm_herbdb.config import Config


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="TCM-HerbDB 命令行工具")
    
    subparsers = parser.add_subparsers(dest="command", help="可用的命令")
    
    # 解析命令
    parse_parser = subparsers.add_parser("parse", help="解析药材数据")
    parse_parser.add_argument("--input", "-i", type=str, default="data/processed/herb.txt",
                              help="输入文件路径")
    parse_parser.add_argument("--output", "-o", type=str, default="output/herbs.csv",
                              help="输出CSV文件路径")
    parse_parser.add_argument("--count", "-c", type=int, default=5,
                              help="显示前n个药材的详细信息")

    # 导出命令
    export_parser = subparsers.add_parser("export", help="导出药材数据到CSV")
    export_parser.add_argument("--input", "-i", type=str, default="data/processed/herb.txt",
                               help="输入文件路径")
    export_parser.add_argument("--output", "-o", type=str, default="output/herbs.csv",
                               help="输出CSV文件路径")
    
    return parser.parse_args()


def cmd_parse(args):
    """执行解析命令"""
    # 确保路径是相对于当前工作目录的
    input_path = project_root / args.input
    print(f"正在从 {input_path} 解析药材数据...")

    # 检查输入文件是否存在
    if not input_path.exists():
        print(f"错误: 找不到输入文件 {input_path}")
        return
    
    # 读取并解析药材数据
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = HerbParser()
    herbs = parser.extract_herb_info(content)
    
    print(f"成功提取了 {len(herbs)} 味药材的信息")
    print()
    
    # 显示前n个药材的详细信息
    print(f"前{args.count}味药材的详细信息:")
    print("-" * 50)
    for i, herb in enumerate(herbs[:args.count]):
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
    
    # 询问是否导出到CSV
    export_choice = input("\n是否导出到CSV文件? (y/N): ")
    if export_choice.lower() == 'y':
        cmd_export(args)


def cmd_export(args):
    """执行导出命令"""
    # 确保路径是相对于当前工作目录的
    input_path = project_root / args.input
    print(f"正在从 {input_path} 加载药材数据...")

    # 检查输入文件是否存在
    if not input_path.exists():
        print(f"错误: 找不到输入文件 {input_path}")
        return
    
    # 创建数据库实例并导出到CSV
    db = ExtendedHerbDatabase.from_txt_file(args.input)
    
    # 确保输出目录存在
    output_path = project_root / args.output
    output_path.parent.mkdir(exist_ok=True)

    # 导出到CSV
    db.export_to_csv(str(output_path))

    print(f"CSV文件已生成: {output_path}")
    print(f"CSV文件大小: {output_path.stat().st_size} 字节")


def main():
    """主函数"""
    args = parse_arguments()
    
    if args.command == "parse":
        cmd_parse(args)
    elif args.command == "export":
        cmd_export(args)
    else:
        print("请指定一个命令: parse 或 export")
        print("使用 --help 查看帮助信息")


if __name__ == "__main__":
    main()