# 贡献指南

感谢您对TCM-HerbDB项目的兴趣！我们欢迎各种形式的贡献，包括但不限于：

- 报告bug
- 提出新功能
- 改进文档
- 提交代码修复
- 单位测试

## 开发环境设置

1. 克隆仓库：
   ```bash
   git clone https://github.com/your-username/TCM-HerbDB.git
   ```

2. 安装依赖：
   ```bash
   uv sync
   ```

3. 安装为可编辑包（用于命令行工具）：
   ```bash
   uv pip install -e .
   ```

4. 运行测试：
   ```bash
   uv run pytest tests/
   ```

## 代码风格

- 遵循 PEP 8 代码风格规范
- 使用类型提示
- 编写清晰的文档字符串
- 采用面向对象设计原则
- 集中管理配置信息

## 项目结构

TCM-HerbDB 采用模块化设计：

```
TCM-HerbDB/
├── cli.py              # 命令行入口点
├── demo.py             # 项目演示脚本
├── src/tcm_herbdb/     # 主要的 Python 包
│   ├── cli.py          # 命令行接口模块
│   ├── config.py       # 配置管理模块
│   ├── database.py     # 数据库操作模块
│   ├── herb_parser.py  # 药材解析器模块
│   └── logging_config.py # 日志配置模块
├── tests/tcm_herbdb/   # 测试模块目录
│   ├── test_herb_database.py      # 数据库类测试
│   ├── test_herb_parser.py        # 解析器类测试
│   └── test_extended_herb_database.py # 扩展数据库类测试
```

## 提交更改

1. 创建功能分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 提交更改：
   ```bash
   git add .
   git commit -m "描述你的更改"
   git push origin feature/your-feature-name
   ```

3. 创建 Pull Request

## 测试

所有代码更改都需要相应的测试。在提交之前，请确保所有测试都通过：

```bash
uv run pytest tests/
```

测试应遵循以下原则：
- 将测试分离到不同的模块中，提高可维护性
- 为每个类和主要功能编写专门的测试
- 确保测试覆盖边界情况和错误处理

## 命令行工具

项目提供命令行工具，支持以下功能：

```bash
# 解析药材数据
uv run python cli.py parse --count 5 --input data/processed/herb.txt --output output/herbs.csv

# 导出药材数据到CSV
uv run python cli.py export --input data/processed/herb.txt --output output/herbs.csv
```

## 问题报告

当报告问题时，请包含：
- Python 版本
- 项目版本
- 重现问题的步骤
- 预期行为和实际行为
- 相关的错误信息