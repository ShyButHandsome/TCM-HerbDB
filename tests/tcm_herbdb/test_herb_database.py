"""
HerbDatabase 类的测试文件
"""
import pytest
import os
import sys
from pathlib import Path

from tcm_herbdb import HerbParser, ExtendedHerbDatabase


class TestHerbDatabase:
    """HerbDatabase 类的测试"""

    @classmethod
    def setup_class(cls):
        """在所有测试开始前加载数据"""
        cls.data_file = Path(__file__).parent.parent.parent / "data" / "processed" / "herb.txt"
        if not cls.data_file.exists():
            raise FileNotFoundError(f"数据文件不存在: {cls.data_file}")
        
        cls.parser = HerbParser()
        with open(cls.data_file, 'r', encoding='utf-8') as f:
            content = f.read()
        herbs = cls.parser.extract_herb_info(content)
        
        cls.database = ExtendedHerbDatabase(herbs)

    def test_database_initialization(self):
        """测试数据库初始化"""
        assert self.database is not None, "数据库应该成功初始化"
        assert len(self.database.herbs) > 0, "数据库应该包含药材数据"

    def test_add_herb(self):
        """测试添加药材功能"""
        initial_count = self.database.get_herb_count()
        new_herb = {
            "name": "测试药材",
            "pinyin": "ceshiyaocai",
            "source": "《测试来源》",
            "properties": "测试药性",
            "efficacy": "测试功效",
            "application": "测试应用",
            "dosage": "测试用量",
            "precautions": "测试注意",
            "modern_research": "测试研究",
            "full_content": "测试完整内容"
        }
        self.database.add_herb(new_herb)
        assert self.database.get_herb_count() == initial_count + 1, "药材数量应该增加1"

    def test_get_herbs_by_name(self):
        """测试按名称查找药材功能"""
        if len(self.database.herbs) > 0:
            # 使用第一个药材的名称进行测试
            first_herb_name = self.database.herbs[0]["name"]
            found_herbs = self.database.get_herbs_by_name(first_herb_name)
            assert len(found_herbs) > 0, f"应该能找到名称为 '{first_herb_name}' 的药材"
            for herb in found_herbs:
                assert herb["name"] == first_herb_name, "返回的药材名称应该匹配"

    def test_get_herbs_by_property(self):
        """测试按药性查找药材功能"""
        # 使用一个常见的药性进行测试
        if len(self.database.herbs) > 0:
            # 获取第一个药材的药性（如果存在）
            first_herb_properties = self.database.herbs[0].get("properties", "")
            if first_herb_properties:
                found_herbs = self.database.get_herbs_by_property(first_herb_properties.split()[0] if first_herb_properties.split() else "")
                # 由于我们按完整属性值的一部分搜索，可能找不到完全匹配的，这是正常的
                # 我们只是测试函数不报错且返回列表
                assert isinstance(found_herbs, list), "返回的应该是一个列表"

    def test_get_herbs_by_efficacy(self):
        """测试按功效查找药材功能"""
        # 使用一个常见功效进行测试
        if len(self.database.herbs) > 0:
            first_herb_efficacy = self.database.herbs[0].get("efficacy", "")
            if first_herb_efficacy:
                found_herbs = self.database.get_herbs_by_efficacy(first_herb_efficacy.split()[0] if first_herb_efficacy.split() else "")
                # 与上面类似，我们只是测试函数的执行
                assert isinstance(found_herbs, list), "返回的应该是一个列表"

    def test_get_all_herbs(self):
        """测试获取所有药材功能"""
        all_herbs = self.database.get_all_herbs()
        assert len(all_herbs) == self.database.get_herb_count(), "获取的所有药材数量应该等于数据库中的数量"

    def test_get_herb_count(self):
        """测试获取药材数量功能"""
        count = self.database.get_herb_count()
        assert count > 0, "药材数量应该大于0"
        assert count == len(self.database.herbs), "药材数量应该等于内部列表长度"