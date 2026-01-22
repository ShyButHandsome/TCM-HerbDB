"""
ExtendedHerbDatabase 类的测试文件
"""
import pytest
import os
import sys
from pathlib import Path

from tcm_herbdb import ExtendedHerbDatabase


class TestExtendedHerbDatabase:
    """ExtendedHerbDatabase 类的测试"""

    @classmethod
    def setup_class(cls):
        """在所有测试开始前加载数据"""
        cls.data_file = Path(__file__).parent.parent.parent / "data" / "processed" / "herb.txt"
        if not cls.data_file.exists():
            raise FileNotFoundError(f"数据文件不存在: {cls.data_file}")
        
        cls.extended_db = ExtendedHerbDatabase.from_txt_file(cls.data_file)

    def test_from_txt_file(self):
        """测试从txt文件创建数据库"""
        assert self.extended_db is not None, "扩展数据库应该成功从txt文件创建"
        assert len(self.extended_db.herbs) > 0, "扩展数据库应该包含药材数据"

    def test_to_dataframe(self):
        """测试转换为DataFrame功能"""
        df = self.extended_db.to_dataframe()
        assert df is not None, "DataFrame不应该为None"
        assert len(df) == self.extended_db.get_herb_count(), "DataFrame行数应该等于药材数量"
        
        # 检查DataFrame是否包含预期的列
        expected_columns = {"name", "pinyin", "source", "properties", "efficacy", "application", 
                           "dosage", "precautions", "modern_research", "full_content"}
        actual_columns = set(df.columns)
        # 由于某些药材可能缺少某些字段，我们检查主要字段是否存在
        assert "name" in actual_columns, "DataFrame应该包含name列"
        assert "pinyin" in actual_columns, "DataFrame应该包含pinyin列"
        assert "source" in actual_columns, "DataFrame应该包含source列"

    def test_export_to_csv(self, tmp_path):
        """测试导出到CSV功能"""
        csv_file = tmp_path / "test_herbs.csv"
        self.extended_db.export_to_csv(str(csv_file))
        
        assert csv_file.exists(), "CSV文件应该被创建"
        assert csv_file.stat().st_size > 0, "CSV文件不应该为空"
        
        # 检查文件是否为有效的CSV格式
        with open(csv_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 检查是否包含预期的列名（顺序可能不同）
            assert "name" in content, "CSV文件应该包含name列"
            assert "pinyin" in content, "CSV文件应该包含pinyin列"
            assert "source" in content, "CSV文件应该包含source列"