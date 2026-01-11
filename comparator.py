"""
字段比对模块
负责比较原始BibTeX和Scholar返回的BibTeX，检测差异
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum


class DifferenceType(Enum):
    """差异类型枚举"""
    MISSING = "missing"  # 原文件缺失该字段
    MISMATCH = "mismatch"  # 字段值不匹配
    MATCH = "match"  # 字段值匹配


class FieldDifference:
    """字段差异类"""
    
    def __init__(self, field_name: str, original_value: Optional[str], 
                 scholar_value: Optional[str], diff_type: DifferenceType):
        self.field_name = field_name
        self.original_value = original_value
        self.scholar_value = scholar_value
        self.diff_type = diff_type
    
    def __repr__(self):
        return f"FieldDifference({self.field_name}: {self.original_value} -> {self.scholar_value})"


class EntryComparison:
    """单个条目的比对结果"""
    
    def __init__(self, citation_key: str, title: str):
        self.citation_key = citation_key
        self.title = title
        self.differences: List[FieldDifference] = []
        self.has_differences = False
        self.title_mismatch = False  # 标记title是否不匹配
        self.scholar_title = None  # Scholar返回的title
    
    def add_difference(self, field_diff: FieldDifference):
        """添加字段差异"""
        self.differences.append(field_diff)
        if field_diff.diff_type in [DifferenceType.MISSING, DifferenceType.MISMATCH]:
            self.has_differences = True
    
    def get_mismatches(self) -> List[FieldDifference]:
        """获取所有不匹配和缺失的字段"""
        return [d for d in self.differences 
                if d.diff_type in [DifferenceType.MISSING, DifferenceType.MISMATCH]]
    
    def __repr__(self):
        return f"EntryComparison({self.citation_key}, differences={len(self.differences)})"


class FieldComparator:
    """字段比对器"""
    
    # 需要比对的字段（排除ID和title）
    FIELDS_TO_COMPARE = [
        'author', 'journal', 'booktitle', 'volume', 'number', 
        'pages', 'year', 'publisher', 'doi', 'organization',
        'address', 'month', 'isbn', 'issn', 'editor', 'series'
    ]
    
    # 不应该比对的字段
    EXCLUDED_FIELDS = ['ID', 'ENTRYTYPE', 'title']
    
    @staticmethod
    def normalize_title(title: str) -> str:
        """
        规范化标题用于比较
        
        Args:
            title: 原始标题
            
        Returns:
            规范化后的标题
        """
        if not title:
            return ""
        
        # 移除LaTeX特殊格式
        title = re.sub(r'\\text\{([^}]+)\}', r'\1', title)
        title = re.sub(r'\{\\text\{([^}]+)\}\}', r'\1', title)
        title = re.sub(r'\{([^}]+)\}', r'\1', title)
        
        # 移除标点符号和特殊字符
        title = re.sub(r'[^\w\s]', ' ', title)
        
        # 转换为小写并统一空格
        title = ' '.join(title.lower().split())
        
        return title
    
    @staticmethod
    def calculate_title_match_score(title1: str, title2: str) -> Tuple[bool, int]:
        """
        计算两个标题的匹配度
        
        Args:
            title1: 标题1
            title2: 标题2
            
        Returns:
            (是否匹配, 不同单词数量)
        """
        # 规范化标题
        norm_title1 = FieldComparator.normalize_title(title1)
        norm_title2 = FieldComparator.normalize_title(title2)
        
        # 如果完全相同（忽略大小写），返回匹配
        if norm_title1 == norm_title2:
            return (True, 0)
        
        # 分割成单词
        words1 = set(norm_title1.split())
        words2 = set(norm_title2.split())
        
        # 计算不同的单词数（对称差集）
        diff_words = words1.symmetric_difference(words2)
        diff_count = len(diff_words)
        
        # 如果不同单词数超过1个，认为不匹配
        is_match = diff_count <= 1
        
        return (is_match, diff_count)
    
    @staticmethod
    def normalize_value(value: str, field_name: str) -> str:
        """
        规范化字段值
        
        Args:
            value: 原始值
            field_name: 字段名
            
        Returns:
            规范化后的值
        """
        if not value:
            return ""
        
        value = str(value).strip()
        
        # 移除LaTeX命令和特殊格式
        value = re.sub(r'\\text\{([^}]+)\}', r'\1', value)
        value = re.sub(r'\{\\text\{([^}]+)\}\}', r'\1', value)
        value = re.sub(r'\{([^}]+)\}', r'\1', value)  # 移除简单花括号
        
        # 处理特殊LaTeX字符
        latex_chars = {
            r"\\'e": 'é', r'\\`e': 'è', r'\\^e': 'ê', r'\\"e': 'ë',
            r"\\'a": 'á', r'\\`a': 'à', r'\\^a': 'â', r'\\"a': 'ä',
            r"\\'o": 'ó', r'\\`o': 'ò', r'\\^o': 'ô', r'\\"o': 'ö',
            r'\\~n': 'ñ', r'\\c{c}': 'ç',
        }
        for latex, char in latex_chars.items():
            value = value.replace(latex, char)
        
        # 字段特定处理
        if field_name == 'pages':
            # 统一页码格式：使用双短横线
            value = re.sub(r'(\d+)\s*-\s*(\d+)', r'\1--\2', value)
            value = re.sub(r'(\d+)\s*–\s*(\d+)', r'\1--\2', value)  # em dash
        
        elif field_name == 'author':
            # 规范化作者名
            value = re.sub(r'\s+', ' ', value)  # 统一空格
            value = re.sub(r'\s*,\s*', ', ', value)  # 规范化逗号
            value = re.sub(r'\s+and\s+', ' and ', value, flags=re.IGNORECASE)
        
        elif field_name in ['journal', 'booktitle']:
            # 期刊和会议名：统一空格
            value = re.sub(r'\s+', ' ', value)
        
        elif field_name == 'year':
            # 只保留数字
            value = re.sub(r'\D', '', value)
        
        return value.strip()
    
    @staticmethod
    def values_are_equal(value1: str, value2: str, field_name: str) -> bool:
        """
        判断两个字段值是否相等
        
        Args:
            value1: 值1
            value2: 值2
            field_name: 字段名
            
        Returns:
            是否相等
        """
        norm1 = FieldComparator.normalize_value(value1, field_name)
        norm2 = FieldComparator.normalize_value(value2, field_name)
        
        # 空值处理
        if not norm1 and not norm2:
            return True
        if not norm1 or not norm2:
            return False
        
        # 对于作者字段，进行更宽松的比较
        if field_name == 'author':
            # 移除所有空格和标点，转换为小写
            comp1 = re.sub(r'[^\w]', '', norm1).lower()
            comp2 = re.sub(r'[^\w]', '', norm2).lower()
            return comp1 == comp2
        
        # 对于年份，只比较数字
        if field_name == 'year':
            return norm1 == norm2
        
        # 其他字段：大小写不敏感比较
        return norm1.lower() == norm2.lower()
    
    @staticmethod
    def compare_entries(original_entry: Dict, scholar_entry: Dict) -> EntryComparison:
        """
        比较两个BibTeX条目
        
        Args:
            original_entry: 原始条目
            scholar_entry: Scholar返回的条目
            
        Returns:
            EntryComparison对象
        """
        citation_key = original_entry.get('ID', 'unknown')
        original_title = original_entry.get('title', 'No title')
        scholar_title = scholar_entry.get('title', '')
        
        comparison = EntryComparison(citation_key, original_title)
        comparison.scholar_title = scholar_title
        
        # 首先检查title匹配度
        is_match, diff_count = FieldComparator.calculate_title_match_score(
            original_title, scholar_title
        )
        
        if not is_match:
            # Title不匹配，标记并跳过其他字段比对
            comparison.title_mismatch = True
            comparison.has_differences = True
            return comparison
        
        # Title匹配，继续比对其他字段
        # 获取所有需要比对的字段
        all_fields = set()
        all_fields.update(original_entry.keys())
        all_fields.update(scholar_entry.keys())
        
        # 移除排除字段
        all_fields = all_fields - set(FieldComparator.EXCLUDED_FIELDS)
        
        # 比对每个字段
        for field in sorted(all_fields):
            original_value = original_entry.get(field, "")
            scholar_value = scholar_entry.get(field, "")
            
            # 跳过两边都为空的字段
            if not original_value and not scholar_value:
                continue
            
            # 确定差异类型
            if not original_value and scholar_value:
                # 原文件缺失该字段
                diff_type = DifferenceType.MISSING
            elif original_value and not scholar_value:
                # Scholar没有该字段，保持原值，不算差异
                continue
            elif FieldComparator.values_are_equal(original_value, scholar_value, field):
                # 值相等
                diff_type = DifferenceType.MATCH
            else:
                # 值不匹配
                diff_type = DifferenceType.MISMATCH
            
            field_diff = FieldDifference(field, original_value, scholar_value, diff_type)
            comparison.add_difference(field_diff)
        
        return comparison
    
    @staticmethod
    def compare_batch(original_entries: List[Dict], 
                     scholar_results: Dict[str, Optional[Dict]]) -> List[EntryComparison]:
        """
        批量比对条目
        
        Args:
            original_entries: 原始条目列表
            scholar_results: Scholar搜索结果，键为标题，值为BibTeX字典
            
        Returns:
            EntryComparison对象列表
        """
        comparisons = []
        
        for original_entry in original_entries:
            title = original_entry.get('title', '')
            
            # 查找对应的Scholar结果
            scholar_entry = scholar_results.get(title)
            
            if scholar_entry is None:
                # 如果Scholar没有找到结果，跳过
                continue
            
            comparison = FieldComparator.compare_entries(original_entry, scholar_entry)
            comparisons.append(comparison)
        
        return comparisons
    
    @staticmethod
    def get_updated_fields(comparison: EntryComparison) -> Dict[str, str]:
        """
        获取需要更新的字段
        
        Args:
            comparison: 比对结果
            
        Returns:
            需要更新的字段字典
        """
        updated_fields = {}
        
        for diff in comparison.get_mismatches():
            if diff.scholar_value:
                updated_fields[diff.field_name] = diff.scholar_value
        
        return updated_fields


def format_comparison_summary(comparisons: List[EntryComparison]) -> str:
    """
    格式化比对摘要
    
    Args:
        comparisons: 比对结果列表
        
    Returns:
        格式化的摘要文本
    """
    total = len(comparisons)
    with_differences = sum(1 for c in comparisons if c.has_differences)
    
    summary = f"\n总共检查了 {total} 条参考文献\n"
    summary += f"发现 {with_differences} 条参考文献存在差异\n"
    
    if with_differences == 0:
        summary += "\n✓ 所有参考文献信息都是准确的！\n"
    
    return summary
