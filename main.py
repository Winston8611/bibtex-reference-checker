#!/usr/bin/env python3
"""
BibTeX参考文献检查与修正工具
主程序入口
"""

import argparse
import sys
import logging
from typing import Optional
from colorama import Fore, Style, init

from parser import BibTeXParser
from scholar_scraper import ScholarScraper
from comparator import FieldComparator
from interactive_review import InteractiveReviewer, display_progress, display_summary
from file_updater import FileUpdater


# 初始化colorama
init(autoreset=True)


def setup_logging(verbose: bool = False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bib_checker.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout) if verbose else logging.NullHandler()
        ]
    )


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='BibTeX参考文献检查与修正工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py reference.bib
  python main.py reference.bib --headless
  python main.py reference.bib --delay 2-5
  python main.py reference.bib --output report.html
        """
    )
    
    parser.add_argument(
        'bibfile',
        help='BibTeX文件路径'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='使用无头浏览器模式（不显示浏览器窗口）'
    )
    
    parser.add_argument(
        '--delay',
        type=str,
        default='2-4',
        help='搜索延迟范围（秒），格式: min-max，默认: 2-4'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='生成HTML报告的输出路径'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细日志'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        help='限制检查的文献数量（用于测试）'
    )
    
    return parser.parse_args()


def parse_delay_range(delay_str: str) -> tuple:
    """解析延迟范围"""
    try:
        parts = delay_str.split('-')
        if len(parts) != 2:
            raise ValueError
        
        min_delay = float(parts[0])
        max_delay = float(parts[1])
        
        if min_delay < 0 or max_delay < min_delay:
            raise ValueError
        
        return (min_delay, max_delay)
    except:
        print(f"{Fore.YELLOW}⚠ 无效的延迟范围格式，使用默认值 2-4{Style.RESET_ALL}")
        return (2, 4)


def print_banner():
    """打印程序横幅"""
    banner = f"""
{Fore.CYAN}{'='*80}
 ____  _ _     _____    __   __  ____ _               _             
| __ )(_) |__ |_   _|__\ \/ / / ___| |__   ___  ___ | | _____ _ __ 
|  _ \| | '_ \  | |/ _ \\  /  | |   | '_ \ / _ \/ __|| |/ / _ \ '__|
| |_) | | |_) | | |  __//  \  | |___| | | |  __/ (__ |   <  __/ |   
|____/|_|_.__/  |_|\___/_/\_\  \____|_| |_|\___|\___||_|\_\___|_|   
                                                                      
         BibTeX参考文献检查与修正工具 v1.0
{'='*80}{Style.RESET_ALL}
"""
    print(banner)


def main():
    """主函数"""
    args = parse_arguments()
    
    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # 打印横幅
    print_banner()
    
    # 解析延迟范围
    delay_range = parse_delay_range(args.delay)
    
    print(f"{Fore.CYAN}正在处理: {args.bibfile}{Style.RESET_ALL}\n")
    
    try:
        # 步骤1: 解析BibTeX文件
        print(f"{Fore.YELLOW}[1/5] 解析BibTeX文件...{Style.RESET_ALL}")
        parser = BibTeXParser(args.bibfile)
        parser.parse()
        entries = parser.get_entries()
        
        if not entries:
            print(f"{Fore.RED}✗ 未找到任何BibTeX条目{Style.RESET_ALL}")
            return 1
        
        # 应用限制（如果指定）
        if args.limit and args.limit < len(entries):
            entries = entries[:args.limit]
            print(f"{Fore.YELLOW}ℹ 限制检查数量: {args.limit} 条{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✓ 找到 {len(entries)} 条参考文献{Style.RESET_ALL}\n")
        
        # 步骤2: 从Google Scholar搜索
        print(f"{Fore.YELLOW}[2/5] 从Google Scholar搜索验证...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}ℹ 延迟范围: {delay_range[0]}-{delay_range[1]}秒{Style.RESET_ALL}")
        print(f"{Fore.CYAN}ℹ 无头模式: {'是' if args.headless else '否'}{Style.RESET_ALL}\n")
        
        # 提取标题
        titles = [entry.get('title', '') for entry in entries if entry.get('title')]
        
        # 搜索
        with ScholarScraper(headless=args.headless, delay_range=delay_range) as scraper:
            scholar_results = scraper.batch_search(titles, progress_callback=display_progress)
        
        successful_searches = sum(1 for v in scholar_results.values() if v is not None)
        print(f"\n{Fore.GREEN}✓ 成功检索 {successful_searches}/{len(titles)} 条{Style.RESET_ALL}\n")
        
        # 步骤3: 比对字段
        print(f"{Fore.YELLOW}[3/5] 比对字段差异...{Style.RESET_ALL}")
        comparisons = FieldComparator.compare_batch(entries, scholar_results)
        
        if not comparisons:
            print(f"{Fore.YELLOW}⚠ 没有可比对的结果{Style.RESET_ALL}")
            return 0
        
        print(f"{Fore.GREEN}✓ 完成比对{Style.RESET_ALL}\n")
        
        # 显示摘要
        display_summary(comparisons)
        
        # 步骤4: 交互式审查
        print(f"\n{Fore.YELLOW}[4/5] 交互式审查...{Style.RESET_ALL}\n")
        reviewer = InteractiveReviewer()
        entries_with_diff, title_mismatch_entries = reviewer.display_differences(comparisons)
        
        # 如果有title不匹配的条目，记录到日志
        if title_mismatch_entries:
            logger.warning(f"发现 {len(title_mismatch_entries)} 条文献标题不匹配")
            for entry in title_mismatch_entries:
                logger.warning(f"  {entry.citation_key}: '{entry.title}' != '{entry.scholar_title}'")
        
        if not entries_with_diff:
            if title_mismatch_entries:
                print(f"\n{Fore.YELLOW}检查完成。{len(title_mismatch_entries)} 条标题不匹配的文献需要人工处理。{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}所有检查完成！无需修改。{Style.RESET_ALL}")
            return 0
        
        # 提示用户选择
        selected_keys = reviewer.prompt_selection(entries_with_diff)
        
        if not selected_keys:
            print(f"\n{Fore.YELLOW}未选择任何修正项，程序结束。{Style.RESET_ALL}")
            return 0
        
        # 确认修改
        if not reviewer.confirm_changes(comparisons, selected_keys):
            print(f"\n{Fore.YELLOW}已取消修改。{Style.RESET_ALL}")
            return 0
        
        # 步骤5: 更新文件
        print(f"\n{Fore.YELLOW}[5/5] 更新文件...{Style.RESET_ALL}\n")
        updater = FileUpdater(parser)
        
        # 创建备份
        updater.create_backup()
        
        # 更新条目
        updated_count = updater.update_entries(comparisons, selected_keys)
        
        # 保存修改
        if updater.save_changes():
            print(f"\n{Fore.GREEN}✓ 成功更新 {updated_count} 条参考文献{Style.RESET_ALL}")
            
            # 保存更新日志
            updater.save_update_log()
            
            # 生成HTML报告（如果指定）
            if args.output:
                updater.generate_html_report(comparisons, selected_keys, args.output)
        else:
            print(f"\n{Fore.RED}✗ 保存失败{Style.RESET_ALL}")
            return 1
        
        # 显示最终摘要
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ 所有任务完成！{Style.RESET_ALL}")
        if title_mismatch_entries:
            print(f"{Fore.YELLOW}⚠ 注意：{len(title_mismatch_entries)} 条文献因标题不匹配未处理，需要人工检查。{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠ 用户中断操作{Style.RESET_ALL}")
        return 130
    
    except FileNotFoundError:
        print(f"{Fore.RED}✗ 错误: 找不到文件 {args.bibfile}{Style.RESET_ALL}")
        return 1
    
    except Exception as e:
        logger.exception("发生错误")
        print(f"\n{Fore.RED}✗ 发生错误: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}详细信息请查看日志文件: bib_checker.log{Style.RESET_ALL}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
