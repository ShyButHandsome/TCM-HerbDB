"""
HerbParser 类的测试文件
"""
import pytest
import os
import sys
from pathlib import Path

from tcm_herbdb import HerbParser


class TestHerbParser:
    """HerbParser 类的测试"""

    @classmethod
    def setup_class(cls):
        """在所有测试开始前加载数据"""
        cls.data_file = Path(__file__).parent.parent.parent / "data" / "processed" / "herb.txt"
        if not cls.data_file.exists():
            raise FileNotFoundError(f"数据文件不存在: {cls.data_file}")
        
        with open(cls.data_file, 'r', encoding='utf-8') as f:
            cls.content = f.read()
        
        cls.parser = HerbParser()
        cls.herbs = cls.parser.extract_herb_info(cls.content)

    def test_parser_can_extract_herbs(self):
        """测试解析器能够提取药材信息"""
        assert len(self.herbs) > 0, "应该能够提取到至少一个药材"
        print(f"成功提取了 {len(self.herbs)} 味药材")

    def test_herb_structure(self):
        """测试提取的药材结构是否正确"""
        if len(self.herbs) > 0:
            herb = self.herbs[0]
            expected_keys = {"name", "pinyin", "source", "properties", "efficacy", "application", 
                           "dosage", "precautions", "modern_research", "full_content"}
            actual_keys = set(herb.keys())
            
            assert expected_keys.issubset(actual_keys), f"药材字典缺少预期键: {expected_keys - actual_keys}"

    def test_herb_name_not_empty(self):
        """测试药材名称不为空"""
        for herb in self.herbs:
            assert herb["name"], f"药材名称不能为空: {herb}"
            assert herb["name"].strip() != "", f"药材名称不能只包含空白字符: {herb}"

    def test_herb_pinyin_not_empty(self):
        """测试药材拼音不为空"""
        for herb in self.herbs:
            assert herb["pinyin"], f"药材拼音不能为空: {herb}"
            assert herb["pinyin"].strip() != "", f"药材拼音不能只包含空白字符: {herb}"

    def test_herb_source_not_empty(self):
        """测试药材来源不为空"""
        for herb in self.herbs:
            assert herb["source"], f"药材来源不能为空: {herb}"
            assert herb["source"].strip() != "", f"药材来源不能只包含空白字符: {herb}"

    def test_extract_section_functionality(self):
        """测试 extract_section 方法的功能"""
        sample_content = """【药性】寒、凉。【功效】清热解毒，凉血消斑。"""
        result = self.parser.extract_section(sample_content, "【药性】")
        assert result == "寒、凉。"
        
        result = self.parser.extract_section(sample_content, "【功效】")
        assert result == "清热解毒，凉血消斑。"

    def test_get_first_n_herbs(self):
        """测试获取前n个药材的功能"""
        n = 5
        first_n_herbs = self.parser.get_first_n_herbs(self.data_file, n)
        assert len(first_n_herbs) == n, f"应该返回{n}个药材"
        assert len(first_n_herbs) <= len(self.herbs), "返回的药材数量不应超过总数量"

    def test_herb_count_reasonable(self):
        """测试药材数量是否在合理范围内"""
        assert 400 <= len(self.herbs) <= 600, f"药材数量 {len(self.herbs)} 不在合理范围内"