import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
from .herb_parser import HerbParser
from .config import Config


class BaseHerbDatabase:
    """
    基础中药数据库管理类
    """

    def __init__(self, herbs: List[Dict[str, str]] = None):
        self.herbs = herbs or []

    def add_herb(self, herb: Dict[str, str]):
        """添加单味药材"""
        self.herbs.append(herb)

    def get_herbs_by_name(self, name: str) -> List[Dict[str, str]]:
        """根据名称查找药材"""
        return [herb for herb in self.herbs if herb['name'] == name]

    def get_herbs_by_property(self, property_value: str) -> List[Dict[str, str]]:
        """根据药性查找药材"""
        return [herb for herb in self.herbs if property_value in herb['properties']]

    def get_herbs_by_efficacy(self, efficacy: str) -> List[Dict[str, str]]:
        """根据功效查找药材"""
        return [herb for herb in self.herbs if efficacy in herb['efficacy']]

    def get_all_herbs(self) -> List[Dict[str, str]]:
        """获取所有药材"""
        return self.herbs

    def get_herb_count(self) -> int:
        """获取药材总数"""
        return len(self.herbs)


class HerbDatabase(BaseHerbDatabase):
    """
    扩展的中药数据库管理类，提供数据导出功能
    """

    def __init__(self, herbs: List[Dict[str, str]] = None):
        super().__init__(herbs)

    def to_dataframe(self) -> pd.DataFrame:
        """
        将药材数据转换为pandas DataFrame
        """
        if not self.herbs:
            return pd.DataFrame()

        # 确保所有字典具有相同的键，以避免DataFrame创建时的问题
        all_keys = set()
        for herb in self.herbs:
            all_keys.update(herb.keys())

        # 用空字符串填充缺失的键
        normalized_herbs = []
        for herb in self.herbs:
            normalized_herb = {key: herb.get(key, "") for key in all_keys}
            normalized_herbs.append(normalized_herb)

        return pd.DataFrame(normalized_herbs)

    def export_to_csv(self, file_path: str, encoding: str = 'utf-8'):
        """
        将药材数据导出到CSV文件
        """
        df = self.to_dataframe()
        df.to_csv(file_path, index=False, encoding=encoding)

    @classmethod
    def from_txt_file(cls, file_path: str):
        """
        从txt文件创建HerbDatabase实例
        """
        parser = HerbParser()
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        herbs = parser.extract_herb_info(content)
        return cls(herbs)