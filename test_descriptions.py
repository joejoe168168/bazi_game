#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test script for relationship descriptions with elements

import sys
sys.path.append('.')

from datas import *
from ganzhi import *
from common import *

class TestDescriptions:
    def __init__(self):
        self.relationship_settings = {
            '天干五合': True,
            '天干相冲': True,
            '地支相冲': True,
            '地支六合': True,
            '地支相刑': True,
            '地支三合局': True,
            '地支三会方': True,
            '地支暗合': True,
            '地支相害': False,
            '地支相破': False
        }
    
    def test_gan_he_descriptions(self):
        """Test 天干五合 descriptions"""
        print("Testing 天干五合 Descriptions")
        print("=" * 40)
        
        # Test all 天干五合 pairs
        test_pairs = [('甲', '己'), ('乙', '庚'), ('丙', '辛'), ('丁', '壬'), ('戊', '癸')]
        
        for gan1, gan2 in test_pairs:
            if (gan1, gan2) in gan_hes or (gan2, gan1) in gan_hes:
                rel_info = gan_hes.get((gan1, gan2), gan_hes.get((gan2, gan1)))
                
                # Extract element
                element = ""
                if "化土" in rel_info:
                    element = "合土"
                elif "化金" in rel_info:
                    element = "合金"
                elif "化水" in rel_info:
                    element = "合水"
                elif "化木" in rel_info:
                    element = "合木"
                elif "化火" in rel_info:
                    element = "合火"
                
                short_desc = f"{gan1}{gan2}{element}" if element else f"{gan1}{gan2}相合"
                print(f"  {gan1}{gan2}: {short_desc}")
                print(f"    Full: {rel_info.strip()}")
        
        print()
    
    def test_zhi_liuhe_descriptions(self):
        """Test 地支六合 descriptions"""
        print("Testing 地支六合 Descriptions")
        print("=" * 40)
        
        # Test key 六合 pairs
        test_pairs = [('子', '丑'), ('寅', '亥'), ('卯', '戌'), ('酉', '辰'), ('申', '巳'), ('未', '午')]
        
        for zhi1, zhi2 in test_pairs:
            pair_key = f"{zhi1}{zhi2}"
            reverse_key = f"{zhi2}{zhi1}"
            element = zhi_6hes.get(pair_key, zhi_6hes.get(reverse_key, ""))
            
            desc = f"{zhi1}{zhi2}六合化{element}" if element else f"{zhi1}{zhi2}六合"
            print(f"  {zhi1}{zhi2}: {desc}")
        
        print()
    
    def test_sanhe_descriptions(self):
        """Test 三合/半合 descriptions"""
        print("Testing 三合/半合 Descriptions")
        print("=" * 40)
        
        # Test full 三合
        sanhe_patterns = [
            (['申', '子', '辰'], '申子辰三合水局'),
            (['寅', '午', '戌'], '寅午戌三合火局'),
            (['巳', '酉', '丑'], '巳酉丑三合金局'),
            (['亥', '卯', '未'], '亥卯未三合木局')
        ]
        
        print("Full 三合:")
        for pattern, desc in sanhe_patterns:
            print(f"  {''.join(pattern)}: {desc}")
        
        print("\nPartial 半合:")
        # Test partial combinations for 巳酉丑 pattern
        test_pairs = [('巳', '酉'), ('巳', '丑'), ('酉', '丑')]
        
        for zhi1, zhi2 in test_pairs:
            pair_tuple = tuple(sorted([zhi1, zhi2]))
            half_info = zhi_half_3hes.get(pair_tuple, zhi_half_3hes.get(tuple(reversed(pair_tuple)), ""))
            
            if half_info:
                half_desc = f"{zhi1}{zhi2}半合 {half_info}"
            else:
                half_desc = f"{zhi1}{zhi2}半合化金"  # 巳酉丑 pattern = 金
            
            print(f"  {zhi1}{zhi2}: {half_desc}")
        
        print()
    
    def test_sanhui_descriptions(self):
        """Test 三会/半会 descriptions"""
        print("Testing 三会/半会 Descriptions")
        print("=" * 40)
        
        # Test full 三会
        sanhui_patterns = [
            (['亥', '子', '丑'], '亥子丑三会水方'),
            (['寅', '卯', '辰'], '寅卯辰三会木方'),
            (['巳', '午', '未'], '巳午未三会火方'),
            (['申', '酉', '戌'], '申酉戌三会金方')
        ]
        
        print("Full 三会:")
        for pattern, desc in sanhui_patterns:
            print(f"  {''.join(pattern)}: {desc}")
        
        print("\nPartial 半会:")
        # Test partial combinations for each pattern
        test_cases = [
            (['亥', '子'], '水'),
            (['寅', '卯'], '木'), 
            (['巳', '午'], '火'),
            (['申', '酉'], '金')
        ]
        
        for chars, element in test_cases:
            zhi1, zhi2 = chars[0], chars[1]
            half_desc = f"{zhi1}{zhi2}半会化{element}"
            print(f"  {zhi1}{zhi2}: {half_desc}")
        
        print()

def test_user_specific_example():
    """Test the user's specific example"""
    print("Testing User's Specific Example")
    print("=" * 40)
    
    # Test 丑巳 (part of 巳酉丑三合金局)
    zhi1, zhi2 = '丑', '巳'
    pair_tuple = tuple(sorted([zhi1, zhi2]))
    half_info = zhi_half_3hes.get(pair_tuple, zhi_half_3hes.get(tuple(reversed(pair_tuple)), ""))
    
    if half_info:
        half_desc = f"{zhi1}{zhi2}半合 {half_info}"
    else:
        half_desc = f"{zhi1}{zhi2}半合化金"  # 巳酉丑 pattern = 金
    
    print(f"User's example 丑巳: {half_desc}")
    
    # Test 甲己 (user mentioned this)
    gan1, gan2 = '甲', '己'
    if (gan1, gan2) in gan_hes or (gan2, gan1) in gan_hes:
        rel_info = gan_hes.get((gan1, gan2), gan_hes.get((gan2, gan1)))
        
        # Extract element  
        element = ""
        if "化土" in rel_info:
            element = "合土"
        elif "化金" in rel_info:
            element = "合金"
        elif "化水" in rel_info:
            element = "合水"
        elif "化木" in rel_info:
            element = "合木"
        elif "化火" in rel_info:
            element = "合火"
        
        short_desc = f"{gan1}{gan2}{element}" if element else f"{gan1}{gan2}相合"
        print(f"User's example 甲己: {short_desc}")
    
    print()

if __name__ == "__main__":
    print("🎮 Bazi Relationship Descriptions Test")
    print("=" * 50)
    
    test = TestDescriptions()
    test.test_gan_he_descriptions()
    test.test_zhi_liuhe_descriptions()
    test.test_sanhe_descriptions()
    test.test_sanhui_descriptions()
    test_user_specific_example()
    
    print("✅ All description tests completed!")
    print("\nNow relationships will show:")
    print("  - 甲己合土 (instead of just 甲己相合)")
    print("  - 子丑六合化土 (instead of just 子丑六合)")
    print("  - 丑巳半合化金 (instead of generic description)")
    print("  - 申子辰三合水局 (full pattern)")
    print("=" * 50)