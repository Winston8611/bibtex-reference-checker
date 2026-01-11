#!/usr/bin/env python3
"""
测试title匹配功能
"""

from comparator import FieldComparator

def test_title_matching():
    """测试title匹配算法"""
    
    print("="*80)
    print("Title匹配测试")
    print("="*80 + "\n")
    
    # 测试用例
    test_cases = [
        {
            "title1": "A fast and elitist multiobjective genetic algorithm: NSGA-II",
            "title2": "A fast and elitist multiobjective genetic algorithm: NSGA-II",
            "expected": True,
            "description": "完全相同"
        },
        {
            "title1": "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II",
            "title2": "A fast and elitist multiobjective genetic algorithm: NSGA-II",
            "expected": True,
            "description": "大小写不同"
        },
        {
            "title1": "A fast and elitist multiobjective genetic algorithm NSGA-II",
            "title2": "A fast and elitist multiobjective genetic algorithm: NSGA-II",
            "expected": True,
            "description": "标点符号不同（1个差异）"
        },
        {
            "title1": "Fast and elitist multiobjective genetic algorithm: NSGA-II",
            "title2": "A fast and elitist multiobjective genetic algorithm: NSGA-II",
            "expected": True,
            "description": "缺少一个单词'A'"
        },
        {
            "title1": "A fast multiobjective genetic algorithm",
            "title2": "A fast and elitist multiobjective genetic algorithm: NSGA-II",
            "expected": False,
            "description": "缺少多个单词（超过1个差异）"
        },
        {
            "title1": "Solving multiobjective optimization problems",
            "title2": "A fast and elitist multiobjective genetic algorithm",
            "expected": False,
            "description": "完全不同的标题"
        },
        {
            "title1": "Sample Article for Testing BibTeX Checker",
            "title2": "Sample Article for Testing Bibliography Checker",
            "expected": False,
            "description": "一个单词不同（BibTeX vs Bibliography，差异2个）"
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        title1 = test["title1"]
        title2 = test["title2"]
        expected = test["expected"]
        description = test["description"]
        
        is_match, diff_count = FieldComparator.calculate_title_match_score(title1, title2)
        
        status = "✓ PASS" if is_match == expected else "✗ FAIL"
        if is_match == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"测试 {i}: {description}")
        print(f"  标题1: {title1}")
        print(f"  标题2: {title2}")
        print(f"  不同单词数: {diff_count}")
        print(f"  匹配结果: {is_match} (预期: {expected})")
        print(f"  状态: {status}")
        print()
    
    print("="*80)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("="*80)

if __name__ == "__main__":
    test_title_matching()
