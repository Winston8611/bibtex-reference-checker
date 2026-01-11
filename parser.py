"""
BibTeX解析模块
负责读取、解析和写入BibTeX文件，同时保留原始格式和引用键
"""

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import re
from typing import Dict, List, Optional


class BibTeXParser:
    """BibTeX文件解析和处理类"""
    
    def __init__(self, filepath: str):
        """
        初始化解析器
        
        Args:
            filepath: BibTeX文件路径
        """
        self.filepath = filepath
        self.database = None
        self.raw_entries = {}  # 保存原始格式的条目
        
    def parse(self) -> BibDatabase:
        """
        解析BibTeX文件
        
        Returns:
            BibDatabase对象
        """
        parser = BibTexParser(common_strings=True)
        parser.ignore_nonstandard_types = False
        parser.homogenize_fields = False  # 保持原始字段名大小写
        
        with open(self.filepath, 'r', encoding='utf-8') as bibtex_file:
            self.database = bibtexparser.load(bibtex_file, parser=parser)
            
        # 保存每个条目的原始格式
        self._extract_raw_entries()
        
        return self.database
    
    def _extract_raw_entries(self):
        """提取每个条目的原始文本格式"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 使用正则表达式提取每个条目
        entry_pattern = r'@(\w+)\{([^,]+),\s*(.*?)\n\}'
        matches = re.finditer(entry_pattern, content, re.DOTALL)
        
        for match in matches:
            entry_type = match.group(1)
            entry_key = match.group(2).strip()
            entry_body = match.group(3)
            
            self.raw_entries[entry_key] = {
                'type': entry_type,
                'key': entry_key,
                'raw_text': match.group(0)
            }
    
    def get_entries(self) -> List[Dict]:
        """
        获取所有BibTeX条目
        
        Returns:
            条目列表，每个条目是一个字典
        """
        if self.database is None:
            self.parse()
        return self.database.entries
    
    def get_entry_by_key(self, key: str) -> Optional[Dict]:
        """
        根据引用键获取条目
        
        Args:
            key: 引用键（如 'coello2005solving'）
            
        Returns:
            条目字典，如果不存在返回None
        """
        if self.database is None:
            self.parse()
            
        for entry in self.database.entries:
            if entry.get('ID') == key:
                return entry
        return None
    
    def update_entry(self, key: str, updated_fields: Dict):
        """
        更新指定条目的字段
        
        Args:
            key: 引用键
            updated_fields: 要更新的字段字典（不包括ID和ENTRYTYPE）
        """
        if self.database is None:
            self.parse()
            
        for entry in self.database.entries:
            if entry.get('ID') == key:
                # 更新字段，但保留ID和ENTRYTYPE
                for field, value in updated_fields.items():
                    if field not in ['ID', 'ENTRYTYPE']:
                        entry[field] = value
                break
    
    def save(self, output_path: Optional[str] = None):
        """
        保存BibTeX数据库到文件
        
        Args:
            output_path: 输出文件路径，如果为None则覆盖原文件
        """
        if self.database is None:
            raise ValueError("No database loaded. Call parse() first.")
        
        output_path = output_path or self.filepath
        
        writer = BibTexWriter()
        writer.indent = '\t'  # 使用制表符缩进
        writer.order_entries_by = None  # 保持原始顺序
        
        with open(output_path, 'w', encoding='utf-8') as bibtex_file:
            bibtex_file.write(writer.write(self.database))
    
    def create_backup(self, backup_suffix: str = '.backup'):
        """
        创建原始文件的备份
        
        Args:
            backup_suffix: 备份文件后缀
        """
        import shutil
        backup_path = self.filepath + backup_suffix
        shutil.copy2(self.filepath, backup_path)
        return backup_path
    
    @staticmethod
    def normalize_field_value(value: str, field_name: str) -> str:
        """
        规范化字段值以便比较
        
        Args:
            value: 字段值
            field_name: 字段名
            
        Returns:
            规范化后的值
        """
        if not value:
            return ""
        
        value = str(value).strip()
        
        # 移除LaTeX特殊字符包围的花括号
        value = re.sub(r'\{\\text\{([^}]+)\}\}', r'\1', value)
        value = re.sub(r'\\text\{([^}]+)\}', r'\1', value)
        
        # 处理页码范围：统一使用双短横线
        if field_name == 'pages':
            value = re.sub(r'(\d+)\s*-\s*(\d+)', r'\1--\2', value)
        
        # 处理作者名：移除多余空格
        if field_name == 'author':
            value = re.sub(r'\s+', ' ', value)
            value = re.sub(r'\s*,\s*', ', ', value)
            value = re.sub(r'\s+and\s+', ' and ', value)
        
        return value
    
    @staticmethod
    def fields_are_equal(value1: str, value2: str, field_name: str) -> bool:
        """
        比较两个字段值是否相等（考虑规范化）
        
        Args:
            value1: 字段值1
            value2: 字段值2
            field_name: 字段名
            
        Returns:
            是否相等
        """
        norm1 = BibTeXParser.normalize_field_value(value1, field_name)
        norm2 = BibTeXParser.normalize_field_value(value2, field_name)
        
        # 对于作者字段，进行更宽松的比较
        if field_name == 'author':
            # 移除所有空格和大小写进行比较
            norm1 = norm1.replace(' ', '').lower()
            norm2 = norm2.replace(' ', '').lower()
        
        return norm1 == norm2


def parse_bibtex_string(bibtex_str: str) -> Dict:
    """
    解析BibTeX字符串为字典
    
    Args:
        bibtex_str: BibTeX格式字符串
        
    Returns:
        解析后的字典
    """
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    
    db = bibtexparser.loads(bibtex_str, parser=parser)
    
    if db.entries:
        return db.entries[0]
    return {}
