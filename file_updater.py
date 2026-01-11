"""
文件更新模块
负责根据用户选择批量更新BibTeX文件
"""

import os
import json
from typing import Dict, List, Set
from datetime import datetime
from parser import BibTeXParser
from comparator import EntryComparison, FieldComparator
from colorama import Fore, Style


class FileUpdater:
    """文件更新类"""
    
    def __init__(self, parser: BibTeXParser):
        """
        初始化文件更新器
        
        Args:
            parser: BibTeX解析器实例
        """
        self.parser = parser
        self.backup_path = None
        self.update_log = []
    
    def create_backup(self) -> str:
        """
        创建备份文件
        
        Returns:
            备份文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = f"{self.parser.filepath}.backup"
        
        # 如果备份文件已存在，添加时间戳
        if os.path.exists(self.backup_path):
            self.backup_path = f"{self.parser.filepath}.backup_{timestamp}"
        
        self.parser.create_backup(self.backup_path.replace(self.parser.filepath, ''))
        
        print(f"{Fore.GREEN}✓ 已创建备份文件: {self.backup_path}{Style.RESET_ALL}")
        return self.backup_path
    
    def update_entries(self, comparisons: List[EntryComparison], 
                      selected_keys: Set[str]) -> int:
        """
        更新选中的条目
        
        Args:
            comparisons: 比对结果列表
            selected_keys: 选中的引用键集合
            
        Returns:
            更新的条目数量
        """
        updated_count = 0
        
        for comparison in comparisons:
            if comparison.citation_key not in selected_keys:
                continue
            
            # 获取需要更新的字段
            updated_fields = FieldComparator.get_updated_fields(comparison)
            
            if not updated_fields:
                continue
            
            # 更新条目
            self.parser.update_entry(comparison.citation_key, updated_fields)
            
            # 记录更新
            self._log_update(comparison, updated_fields)
            updated_count += 1
            
            print(f"{Fore.GREEN}✓ 已更新: {comparison.citation_key}{Style.RESET_ALL}")
        
        return updated_count
    
    def _log_update(self, comparison: EntryComparison, updated_fields: Dict[str, str]):
        """记录更新信息"""
        log_entry = {
            'citation_key': comparison.citation_key,
            'title': comparison.title,
            'timestamp': datetime.now().isoformat(),
            'updated_fields': {}
        }
        
        # 获取原始值
        original_entry = self.parser.get_entry_by_key(comparison.citation_key)
        
        for field, new_value in updated_fields.items():
            original_value = original_entry.get(field, '') if original_entry else ''
            log_entry['updated_fields'][field] = {
                'original': original_value,
                'new': new_value
            }
        
        self.update_log.append(log_entry)
    
    def save_changes(self, output_path: str = None) -> bool:
        """
        保存修改到文件
        
        Args:
            output_path: 输出文件路径，如果为None则覆盖原文件
            
        Returns:
            是否成功保存
        """
        try:
            self.parser.save(output_path)
            
            save_path = output_path or self.parser.filepath
            print(f"\n{Fore.GREEN}✓ 修改已保存到: {save_path}{Style.RESET_ALL}")
            
            return True
        except Exception as e:
            print(f"\n{Fore.RED}✗ 保存失败: {str(e)}{Style.RESET_ALL}")
            return False
    
    def save_update_log(self, log_path: str = None):
        """
        保存更新日志
        
        Args:
            log_path: 日志文件路径
        """
        if not self.update_log:
            return
        
        if log_path is None:
            log_path = f"{self.parser.filepath}.update_log.json"
        
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(self.update_log, f, indent=2, ensure_ascii=False)
            
            print(f"{Fore.CYAN}ℹ 更新日志已保存到: {log_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ 无法保存更新日志: {str(e)}{Style.RESET_ALL}")
    
    def generate_html_report(self, comparisons: List[EntryComparison], 
                           selected_keys: Set[str], output_path: str):
        """
        生成HTML格式的差异报告
        
        Args:
            comparisons: 比对结果列表
            selected_keys: 选中的引用键集合
            output_path: 输出文件路径
        """
        html_content = self._generate_html_content(comparisons, selected_keys)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"{Fore.CYAN}ℹ HTML报告已生成: {output_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ 无法生成HTML报告: {str(e)}{Style.RESET_ALL}")
    
    def _generate_html_content(self, comparisons: List[EntryComparison], 
                               selected_keys: Set[str]) -> str:
        """生成HTML内容"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 分离title不匹配和正常差异
        title_mismatch_entries = [c for c in comparisons if c.title_mismatch]
        normal_diff_entries = [c for c in comparisons if c.has_differences and not c.title_mismatch]
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BibTeX差异报告</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .warning-section {{
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 15px;
            margin: 20px 0;
        }}
        .warning-section h2 {{
            color: #e65100;
            margin-top: 0;
        }}
        .entry {{
            border: 1px solid #ddd;
            margin: 20px 0;
            border-radius: 5px;
            overflow: hidden;
        }}
        .entry-header {{
            background-color: #f0f0f0;
            padding: 15px;
            font-weight: bold;
        }}
        .entry-header.selected {{
            background-color: #c8e6c9;
        }}
        .entry-header.title-mismatch {{
            background-color: #ffcdd2;
        }}
        .entry-body {{
            padding: 15px;
        }}
        .difference {{
            margin: 10px 0;
            padding: 10px;
            border-left: 3px solid #ff9800;
            background-color: #fff3e0;
        }}
        .difference.missing {{
            border-left-color: #ffc107;
            background-color: #fff9c4;
        }}
        .difference.mismatch {{
            border-left-color: #f44336;
            background-color: #ffebee;
        }}
        .field-name {{
            font-weight: bold;
            color: #1976d2;
        }}
        .value {{
            font-family: monospace;
            background-color: #f5f5f5;
            padding: 3px 6px;
            border-radius: 3px;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
        .title-comparison {{
            margin: 10px 0;
            padding: 10px;
            background-color: #ffebee;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>BibTeX参考文献差异报告</h1>
        <p class="timestamp">生成时间: {timestamp}</p>
        
        <div class="summary">
            <h2>摘要</h2>
            <p>总共检查: {len(comparisons)} 条参考文献</p>
            <p>标题不匹配: {len(title_mismatch_entries)} 条</p>
            <p>字段差异: {len(normal_diff_entries)} 条</p>
            <p>选择修正: {len(selected_keys)} 条</p>
        </div>
"""
        
        # 添加title不匹配的警告部分
        if title_mismatch_entries:
            html += """
        <div class="warning-section">
            <h2>⚠ 标题不匹配警告</h2>
            <p>以下文献在Google Scholar搜索到的标题与原始标题不匹配（差异超过1个单词），<strong>未对这些文献进行修正</strong>，需要人工检查：</p>
"""
            for entry in title_mismatch_entries:
                html += f"""
            <div class="entry">
                <div class="entry-header title-mismatch">
                    {entry.citation_key} [需要人工检查]
                </div>
                <div class="entry-body">
                    <div class="title-comparison">
                        <p><strong>原始标题:</strong><br><span class="value">{entry.title}</span></p>
                        <p><strong>Scholar标题:</strong><br><span class="value">{entry.scholar_title or '(未找到)'}</span></p>
                    </div>
                </div>
            </div>
"""
            html += """
        </div>
"""
        
        html += """
        <h2>字段差异详情</h2>
"""
        
        # 添加每个条目的详细信息（只显示正常差异，不包括title不匹配的）
        for comparison in comparisons:
            # 跳过title不匹配的条目
            if comparison.title_mismatch:
                continue
                
            if not comparison.has_differences:
                continue
            
            is_selected = comparison.citation_key in selected_keys
            selected_class = "selected" if is_selected else ""
            selected_text = " [已选择修正]" if is_selected else ""
            
            html += f"""
        <div class="entry">
            <div class="entry-header {selected_class}">
                {comparison.citation_key}{selected_text}
            </div>
            <div class="entry-body">
                <p><strong>标题:</strong> {comparison.title}</p>
"""
            
            for diff in comparison.get_mismatches():
                diff_class = diff.diff_type.value
                diff_label = "缺失字段" if diff_class == "missing" else "不匹配"
                
                html += f"""
                <div class="difference {diff_class}">
                    <p><span class="field-name">{diff.field_name}</span> - {diff_label}</p>
                    <p>原始值: <span class="value">{diff.original_value or '(无)'}</span></p>
                    <p>Scholar值: <span class="value">{diff.scholar_value or '(无)'}</span></p>
                </div>
"""
            
            html += """
            </div>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        return html
    
    def rollback(self):
        """回滚到备份文件"""
        if not self.backup_path or not os.path.exists(self.backup_path):
            print(f"{Fore.RED}✗ 找不到备份文件，无法回滚{Style.RESET_ALL}")
            return False
        
        try:
            import shutil
            shutil.copy2(self.backup_path, self.parser.filepath)
            print(f"{Fore.GREEN}✓ 已从备份恢复: {self.backup_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ 回滚失败: {str(e)}{Style.RESET_ALL}")
            return False
