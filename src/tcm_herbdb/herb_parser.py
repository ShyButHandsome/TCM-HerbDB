import re
import logging
from typing import List, Dict, Optional
from .config import Config


# 创建模块日志记录器
logger = logging.getLogger(__name__)


class HerbParser:
    """
    中药信息解析器类
    """

    def __init__(self, pattern: str = None):
        self.pattern = pattern or Config.PARSER_PATTERN

    def extract_herb_info(self, text: str) -> List[Dict[str, str]]:
        """
        从txt文本中提取中药信息，使用提供的正则表达式
        """
        logger.info("开始提取中药信息")
        herbs = []

        # 需要多行匹配
        matches = list(re.finditer(self.pattern, text, re.MULTILINE))
        logger.debug(f"找到 {len(matches)} 个匹配项")

        # 创建一个列表，包含所有匹配的位置和信息
        herb_positions = []
        for match in matches:
            name = match.group(1).strip()
            pinyin = match.group(2).strip()
            source = "《" + match.group(3).strip() + "》"  # 重新添加《》
            herb_positions.append({
                'start': match.start(),
                'end': match.end(),
                'name': name,
                'pinyin': pinyin,
                'source': source
            })

        # 遍历每个药材条目，提取完整内容
        for i, herb_pos in enumerate(herb_positions):
            # 确定当前条目的开始位置
            # 找到当前匹配项后，实际药材条目是从匹配行的下一行开始的
            start_pos = herb_pos['start']
            # 向后查找，找到下一个换行符，然后是药材信息的开始
            newline_pos = text.find('\n', start_pos)
            if newline_pos != -1:
                start_pos = newline_pos + 1

            # 确定当前条目的结束位置
            if i < len(herb_positions) - 1:
                # 下一个药材条目的开始就是当前条目的结束
                end_pos = herb_positions[i + 1]['start']
            else:
                # 如果是最后一个药材，结束位置是文本末尾
                end_pos = len(text)

            # 提取完整内容
            herb_content = text[start_pos:end_pos]

            # 提取各个部分
            parts = {
                "name": herb_pos['name'],
                "pinyin": herb_pos['pinyin'],
                "source": herb_pos['source'],
                "properties": self.extract_section(herb_content, "【药性】"),
                "efficacy": self.extract_section(herb_content, "【功效】"),
                "application": self.extract_section(herb_content, "【应用】"),
                "dosage": self.extract_section(herb_content, "【用法用量】"),
                "precautions": self.extract_section(herb_content, "【使用注意】"),
                "modern_research": self.extract_section(herb_content, "【现代研究】"),
                "full_content": herb_content
            }

            # 过滤掉不需要的条目，如"附药"、"附方"等
            if not (parts["name"].startswith("附药") or parts["name"].startswith("附方") or parts["name"].startswith("附录")):
                herbs.append(parts)
            else:
                logger.debug(f"跳过过滤条目: {parts['name']}")

        logger.info(f"成功提取 {len(herbs)} 味中药信息")
        return herbs

    def extract_section(self, content: str, section_title: str) -> str:
        """
        提取指定标题下的内容
        """
        pattern = f'{re.escape(section_title)}(.*?)(?=【|$)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def get_first_n_herbs(self, file_path: str, n: int = 5) -> List[Dict[str, str]]:
        """
        从文件中提取前n味药材的完整信息
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        herbs = self.extract_herb_info(content)
        return herbs[:n]


class HerbDatabase:
    """
    中药数据库管理类
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


def extract_section(content: str, section_title: str) -> str:
    """
    提取指定标题下的内容（保持向后兼容）
    """
    pattern = f'{re.escape(section_title)}(.*?)(?=【|$)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


# 保持向后兼容性的函数
def extract_herb_info(text: str) -> List[Dict[str, str]]:
    """
    从txt文本中提取中药信息，使用提供的正则表达式
    """
    parser = HerbParser()
    return parser.extract_herb_info(text)


def extract_herb_info_from_txt(text: str) -> List[Dict[str, str]]:
    """
    从纯txt文本中提取中药信息（与extract_herb_info功能相同，保持向后兼容）
    """
    return extract_herb_info(text)


def get_first_n_herbs(file_path: str, n: int = 5) -> List[Dict[str, str]]:
    """
    从文件中提取前n味药材的完整信息
    """
    parser = HerbParser()
    return parser.get_first_n_herbs(file_path, n)


def get_first_n_herbs_from_txt(file_path: str, n: int = 5) -> List[Dict[str, str]]:
    """
    从txt文件中提取前n味药材的完整信息（与get_first_n_herbs功能相同，保持向后兼容）
    """
    return get_first_n_herbs(file_path, n)