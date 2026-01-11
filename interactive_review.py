"""
交互式审查界面模块
提供批量审查和选择差异修正的功能
"""

from typing import List, Dict, Set
from tabulate import tabulate
from colorama import Fore, Style, init
from comparator import EntryComparison, DifferenceType

# 初始化colorama
init(autoreset=True)


class InteractiveReviewer:
    """交互式审查类"""
    
    def __init__(self):
        self.selected_keys: Set[str] = set()
    
    def display_differences(self, comparisons: List[EntryComparison]) -> tuple:
        """
        显示所有差异并允许用户选择
        
        Args:
            comparisons: 比对结果列表
            
        Returns:
            (有差异的条目列表, title不匹配的条目列表)
        """
        # 分离title不匹配的条目和正常差异条目
        title_mismatch_entries = [c for c in comparisons if c.title_mismatch]
        normal_diff_entries = [c for c in comparisons if c.has_differences and not c.title_mismatch]
        
        # 先显示title不匹配的条目
        if title_mismatch_entries:
            self._display_title_mismatches(title_mismatch_entries)
        
        # 再显示正常差异
        if not normal_diff_entries:
            if not title_mismatch_entries:
                print(f"\n{Fore.GREEN}✓ 所有参考文献信息都是准确的！{Style.RESET_ALL}\n")
            return ([], title_mismatch_entries)
        
        print(f"\n{Fore.YELLOW}发现 {len(normal_diff_entries)} 条参考文献存在字段差异：{Style.RESET_ALL}\n")
        
        # 显示详细差异
        self._display_detailed_differences(normal_diff_entries)
        
        return (normal_diff_entries, title_mismatch_entries)
    
    def _display_title_mismatches(self, comparisons: List[EntryComparison]):
        """显示title不匹配的条目"""
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.RED}⚠ 警告：发现 {len(comparisons)} 条文献标题不匹配！{Style.RESET_ALL}")
        print(f"{Fore.RED}这些文献可能在Google Scholar搜索到了错误的结果，将不会对其进行修正。{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}\n")
        
        table_data = []
        for comparison in comparisons:
            table_data.append([
                f"{Fore.CYAN}{comparison.citation_key}{Style.RESET_ALL}",
                self._truncate_text(comparison.title, 50),
                self._truncate_text(comparison.scholar_title or "(未找到)", 50)
            ])
        
        headers = ["Citation Key", "原始标题", "Scholar搜索到的标题"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\n{Fore.YELLOW}这些条目需要人工检查和修正。{Style.RESET_ALL}\n")
    
    def _display_detailed_differences(self, comparisons: List[EntryComparison]):
        """显示详细的字段差异（不包括title不匹配的）"""
        table_data = []
        
        for comparison in comparisons:
            # 跳过title不匹配的条目
            if comparison.title_mismatch:
                continue
                
            mismatches = comparison.get_mismatches()
            
            for i, diff in enumerate(mismatches):
                # 格式化差异类型
                if diff.diff_type == DifferenceType.MISSING:
                    diff_marker = f"{Fore.YELLOW}⚠ 缺失{Style.RESET_ALL}"
                elif diff.diff_type == DifferenceType.MISMATCH:
                    diff_marker = f"{Fore.RED}✗ 不匹配{Style.RESET_ALL}"
                else:
                    continue
                
                # 第一行显示引用键和标题
                if i == 0:
                    citation_info = f"{Fore.CYAN}{comparison.citation_key}{Style.RESET_ALL}"
                    title_info = self._truncate_text(comparison.title, 40)
                else:
                    citation_info = ""
                    title_info = ""
                
                # 格式化字段值
                original_val = self._truncate_text(diff.original_value or "(无)", 30)
                scholar_val = self._truncate_text(diff.scholar_value or "(无)", 30)
                
                table_data.append([
                    citation_info,
                    title_info,
                    diff.field_name,
                    diff_marker,
                    original_val,
                    scholar_val
                ])
        
        headers = ["Citation Key", "标题", "字段", "状态", "原始值", "Scholar值"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """截断过长的文本"""
        if not text:
            return ""
        text = str(text)
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def prompt_selection(self, comparisons: List[EntryComparison]) -> Set[str]:
        """
        提示用户选择要修正的条目
        
        Args:
            comparisons: 有差异的条目列表
            
        Returns:
            选中的引用键集合
        """
        if not comparisons:
            return set()
        
        print(f"\n{Fore.CYAN}请选择要修正的参考文献：{Style.RESET_ALL}")
        print("[A] 全部修正")
        print("[N] 全部不修正")
        print("[S] 单独选择")
        print("[V] 查看详细信息")
        
        while True:
            choice = input(f"\n{Fore.GREEN}请输入选项 (A/N/S/V): {Style.RESET_ALL}").strip().upper()
            
            if choice == 'A':
                # 全选
                self.selected_keys = {c.citation_key for c in comparisons}
                print(f"\n{Fore.GREEN}已选择全部 {len(self.selected_keys)} 条参考文献{Style.RESET_ALL}")
                return self.selected_keys
            
            elif choice == 'N':
                # 全不选
                self.selected_keys = set()
                print(f"\n{Fore.YELLOW}已取消所有修正{Style.RESET_ALL}")
                return self.selected_keys
            
            elif choice == 'S':
                # 单独选择
                return self._individual_selection(comparisons)
            
            elif choice == 'V':
                # 查看详细信息
                self._display_detailed_view(comparisons)
                continue
            
            else:
                print(f"{Fore.RED}无效选项，请重新输入{Style.RESET_ALL}")
    
    def _individual_selection(self, comparisons: List[EntryComparison]) -> Set[str]:
        """单独选择模式"""
        self.selected_keys = set()
        
        print(f"\n{Fore.CYAN}单独选择模式{Style.RESET_ALL}")
        print("对于每条参考文献，输入 Y 修正，N 跳过，Q 完成选择\n")
        
        for i, comparison in enumerate(comparisons, 1):
            # 显示条目信息
            print(f"\n{Fore.CYAN}[{i}/{len(comparisons)}] {comparison.citation_key}{Style.RESET_ALL}")
            print(f"标题: {self._truncate_text(comparison.title, 80)}")
            
            # 显示差异
            mismatches = comparison.get_mismatches()
            for diff in mismatches:
                if diff.diff_type == DifferenceType.MISSING:
                    print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} {diff.field_name}: (无) → {diff.scholar_value}")
                elif diff.diff_type == DifferenceType.MISMATCH:
                    print(f"  {Fore.RED}✗{Style.RESET_ALL} {diff.field_name}: {diff.original_value} → {diff.scholar_value}")
            
            while True:
                choice = input(f"\n修正此条目？ (Y/N/Q): ").strip().upper()
                
                if choice == 'Y':
                    self.selected_keys.add(comparison.citation_key)
                    print(f"{Fore.GREEN}✓ 已选择{Style.RESET_ALL}")
                    break
                elif choice == 'N':
                    print(f"{Fore.YELLOW}跳过{Style.RESET_ALL}")
                    break
                elif choice == 'Q':
                    print(f"\n{Fore.CYAN}完成选择，共选择 {len(self.selected_keys)} 条{Style.RESET_ALL}")
                    return self.selected_keys
                else:
                    print(f"{Fore.RED}无效输入，请输入 Y, N 或 Q{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}完成选择，共选择 {len(self.selected_keys)} 条{Style.RESET_ALL}")
        return self.selected_keys
    
    def _display_detailed_view(self, comparisons: List[EntryComparison]):
        """显示详细视图"""
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}详细信息{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        for i, comparison in enumerate(comparisons, 1):
            print(f"{Fore.YELLOW}[{i}] {comparison.citation_key}{Style.RESET_ALL}")
            print(f"标题: {comparison.title}\n")
            
            mismatches = comparison.get_mismatches()
            for diff in mismatches:
                print(f"  字段: {Fore.CYAN}{diff.field_name}{Style.RESET_ALL}")
                print(f"    原始值:  {diff.original_value or '(无)'}")
                print(f"    Scholar值: {diff.scholar_value or '(无)'}")
                
                if diff.diff_type == DifferenceType.MISSING:
                    print(f"    状态: {Fore.YELLOW}原文件缺失此字段{Style.RESET_ALL}")
                elif diff.diff_type == DifferenceType.MISMATCH:
                    print(f"    状态: {Fore.RED}字段值不匹配{Style.RESET_ALL}")
                print()
            
            print(f"{'-'*80}\n")
    
    def confirm_changes(self, comparisons: List[EntryComparison], 
                       selected_keys: Set[str]) -> bool:
        """
        确认修改
        
        Args:
            comparisons: 所有比对结果
            selected_keys: 选中的引用键
            
        Returns:
            是否确认修改
        """
        if not selected_keys:
            print(f"\n{Fore.YELLOW}没有选择任何条目，不会进行修改{Style.RESET_ALL}")
            return False
        
        # 显示将要修改的条目摘要
        print(f"\n{Fore.CYAN}将要修改以下 {len(selected_keys)} 条参考文献：{Style.RESET_ALL}\n")
        
        selected_comparisons = [c for c in comparisons if c.citation_key in selected_keys]
        
        for comparison in selected_comparisons:
            mismatches = comparison.get_mismatches()
            field_count = len(mismatches)
            print(f"  • {comparison.citation_key} ({field_count} 个字段)")
        
        print(f"\n{Fore.YELLOW}注意：原文件将被备份，扩展名为 .backup{Style.RESET_ALL}")
        
        while True:
            choice = input(f"\n{Fore.GREEN}确认修改？(Y/N): {Style.RESET_ALL}").strip().upper()
            
            if choice == 'Y':
                return True
            elif choice == 'N':
                print(f"{Fore.YELLOW}已取消修改{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.RED}无效输入，请输入 Y 或 N{Style.RESET_ALL}")


def display_progress(current: int, total: int):
    """
    显示进度条
    
    Args:
        current: 当前进度
        total: 总数
    """
    percentage = int(current / total * 100)
    filled = int(current / total * 50)
    bar = '█' * filled + '░' * (50 - filled)
    
    print(f"\r🔍 检查进度: [{bar}] {percentage}% ({current}/{total})", end='', flush=True)
    
    if current == total:
        print()  # 完成后换行


def display_summary(comparisons: List[EntryComparison]):
    """
    显示摘要信息
    
    Args:
        comparisons: 比对结果列表
    """
    total = len(comparisons)
    with_differences = sum(1 for c in comparisons if c.has_differences)
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}检查摘要{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    print(f"总共检查: {total} 条参考文献")
    print(f"发现差异: {with_differences} 条")
    print(f"准确无误: {total - with_differences} 条")
    
    if with_differences == 0:
        print(f"\n{Fore.GREEN}✓ 所有参考文献信息都是准确的！{Style.RESET_ALL}\n")
