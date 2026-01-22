# TCM-HerbDB

TCM-HerbDB 是一个旨在将《中药学》教材中的药材结构化，并构建可查询、可扩展的中药数据库的项目。

## 功能特性

*   **药材信息提取**: 从《中药学》教材的文本文件中提取结构化的药材信息
*   **面向对象设计**: 采用面向对象编程，提供 `HerbParser` 和 `HerbDatabase` 类
*   **数据导出**: 将药材信息导出为CSV格式，便于进一步分析和处理
*   **命令行工具**: 提供命令行接口，支持解析和导出功能
*   **配置管理**: 集中管理应用配置和默认路径

## 项目结构

```
TCM-HerbDB/
├── pyproject.toml      # uv 项目配置文件
├── README.md           # 项目说明文件
├── .gitignore          # Git 忽略文件配置
├── .python-version     # Python 版本指定
├── cli.py              # 命令行入口点
├── data/               # 存放数据文件
│   ├── raw/            # 存放原始数据文件 (如 herb.md)
│   ├── processed/      # 存放处理后的数据文件
│   ├── interim/        # 存放中间处理步骤的数据
│   └── external/       # 存放外部来源的数据
├── demo.py             # 项目演示脚本
├── output/             # 输出文件目录
├── scripts/            # 存放脚本文件 (如数据处理脚本)
├── src/                # 源代码目录
│   └── tcm_herbdb/     # 主要的 Python 包
│       ├── __init__.py
│       ├── cli.py      # 命令行接口模块
│       ├── config.py   # 配置管理模块
│       ├── database.py # 数据库操作模块
│       ├── herb_parser.py # 药材解析器模块
│       ├── logging_config.py # 日志配置模块
│       └── py.typed    # 类型提示标记文件
├── tests/              # 存放测试文件
│   └── tcm_herbdb/     # 测试模块目录
│       ├── test_herb_database.py      # 数据库类测试
│       ├── test_herb_parser.py        # 解析器类测试
│       └── test_extended_herb_database.py # 扩展数据库类测试
└── QWEN.md             # 项目上下文说明文件
```

## 安装与使用

### 环境要求

*   Python 3.13+
*   uv 包管理器

### 安装依赖

```bash
uv sync
```

### 运行脚本

```bash
# 使用命令行工具解析药材数据
uv run python cli.py parse --count 5

# 使用命令行工具导出药材数据到CSV
uv run python cli.py export

# 运行演示脚本
uv run python demo.py

# 运行测试
uv run pytest tests/
```

### 命令行工具使用

```bash
# 解析药材数据并显示前5个药材的详细信息
uv run python cli.py parse --count 5 --input data/processed/herb.txt --output output/herbs.csv

# 导出药材数据到CSV文件
uv run python cli.py export --input data/processed/herb.txt --output output/herbs.csv
```

## 数据来源

项目使用 `data/processed/herb.txt` 作为数据源，该文件包含了《中药学》教材中的药材详细信息。

根据教材内容，各论共收载全国各地常用中药568味，具体分类如下：
*   **掌握药**: 133味
*   **熟悉药**: 98味
*   **了解药**: 114味
*   **参考药**: 98味
*   **附药**: 125味

## 输出文件

*   `output/herbs.csv`: 包含所有药材的完整信息

## 使用示例

以下是如何使用本项目提取和查询药材信息的示例：

```python
from tcm_herbdb import HerbParser, ExtendedHerbDatabase

# 创建解析器实例
parser = HerbParser()

# 读取并解析药材数据
with open('data/processed/herb.txt', 'r', encoding='utf-8') as f:
    content = f.read()

herbs = parser.extract_herb_info(content)

# 查看提取的药材数量
print(f"成功提取了 {len(herbs)} 味药材的信息")

# 查看第一味药材的详细信息
first_herb = herbs[0]
print(f"药材名: {first_herb['name']}")
print(f"拼音: {first_herb['pinyin']}")
print(f"来源: {first_herb['source']}")
print(f"药性: {first_herb['properties']}")
print(f"功效: {first_herb['efficacy']}")

# 使用数据库类管理药材数据
db = ExtendedHerbDatabase(herbs)

# 导出到CSV
db.export_to_csv('output/herbs.csv')
```

## 贡献

我们欢迎各种形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目。

如需报告问题或提出功能请求，请使用 GitHub Issues。

## 开发

项目遵循 PEP 8 代码风格，使用 Git 进行版本控制。

## 许可证

MIT License

Copyright (c) 2025 ShyButHandsome

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.