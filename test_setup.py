#!/usr/bin/env python3
"""
简单测试脚本 - 验证依赖和基本功能
"""

import sys

def test_imports():
    """测试所有依赖是否正确安装"""
    print("测试依赖导入...")
    
    tests = [
        ("bibtexparser", "BibTeX解析库"),
        ("selenium", "Selenium浏览器自动化"),
        ("webdriver_manager", "WebDriver管理器"),
        ("colorama", "彩色终端输出"),
        ("tabulate", "表格显示"),
    ]
    
    failed = []
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"  ✓ {description} ({module})")
        except ImportError:
            print(f"  ✗ {description} ({module}) - 未安装")
            failed.append(module)
    
    if failed:
        print(f"\n错误: 以下依赖未安装: {', '.join(failed)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("\n✓ 所有依赖已正确安装!")
    return True


def test_modules():
    """测试内部模块是否可导入"""
    print("\n测试内部模块...")
    
    try:
        from parser import BibTeXParser
        print("  ✓ parser.py")
        
        from scholar_scraper import ScholarScraper
        print("  ✓ scholar_scraper.py")
        
        from comparator import FieldComparator
        print("  ✓ comparator.py")
        
        from interactive_review import InteractiveReviewer
        print("  ✓ interactive_review.py")
        
        from file_updater import FileUpdater
        print("  ✓ file_updater.py")
        
        print("\n✓ 所有模块正常!")
        return True
        
    except Exception as e:
        print(f"\n✗ 模块导入失败: {str(e)}")
        return False


def test_chrome_driver():
    """测试ChromeDriver是否可用"""
    print("\n测试ChromeDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("  正在下载/验证ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        print("  ✓ ChromeDriver已就绪")
        return True
        
    except Exception as e:
        print(f"  ✗ ChromeDriver测试失败: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("="*60)
    print("BibTeX Reference Checker - 环境测试")
    print("="*60 + "\n")
    
    # 测试依赖
    if not test_imports():
        return 1
    
    # 测试模块
    if not test_modules():
        return 1
    
    # 测试ChromeDriver
    if not test_chrome_driver():
        print("\n警告: ChromeDriver未就绪，但可以在首次运行时自动下载")
    
    print("\n" + "="*60)
    print("✓ 环境测试完成! 可以运行主程序了。")
    print("="*60)
    print("\n使用方法: python main.py <your_bib_file.bib>")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
