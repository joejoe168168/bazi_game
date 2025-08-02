#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Direct test of relationship detection

import sys
sys.path.append('.')

from datas import *
from ganzhi import *
from common import *

def mock_detect_all_relationships(chart):
    """Mock the detect_all_relationships method"""
    relationships = []
    zhis = chart['zhis']
    num_pillars = len(zhis)
    
    # Check Zhi 六合 relationships
    for i in range(num_pillars):
        for j in range(i+1, num_pillars):
            zhi1, zhi2 = zhis[i], zhis[j]
            
            # Check 六合
            if zhi_atts[zhi1]['六'] == zhi2:
                pair_key = f"{zhi1}{zhi2}"
                reverse_key = f"{zhi2}{zhi1}"
                element = zhi_6hes.get(pair_key, zhi_6hes.get(reverse_key, ""))
                desc = f"{zhi1}{zhi2}六合化{element}" if element else f"{zhi1}{zhi2}六合"
                
                relationships.append({
                    'type': '地支六合',
                    'positions': [i, j],
                    'characters': [zhi1, zhi2],
                    'description': desc,
                    'points': 12
                })
    
    # Check 三会 patterns for 半会
    sanhui_patterns = [
        (['亥', '子', '丑'], '亥子丑三会水方'),
        (['寅', '卯', '辰'], '寅卯辰三会木方'),
        (['巳', '午', '未'], '巳午未三会火方'),
        (['申', '酉', '戌'], '申酉戌三会金方')
    ]
    
    for pattern, desc in sanhui_patterns:
        positions = []
        for i, zhi in enumerate(zhis[:num_pillars]):
            if zhi in pattern:
                positions.append(i)
        
        if len(positions) >= 2:
            chars = [zhis[i] for i in positions]
            unique_chars = list(set(chars))
            
            # Handle cases with duplicates
            if len(positions) > len(unique_chars) and len(unique_chars) == 2:
                # Find positions of unique characters
                unique_positions = []
                seen_chars = set()
                for i in positions:
                    char = zhis[i]
                    if char not in seen_chars:
                        unique_positions.append(i)
                        seen_chars.add(char)
                
                if len(unique_positions) == 2:
                    unique_chars_list = [zhis[i] for i in unique_positions]
                    element = ""
                    if set(pattern) == {'巳', '午', '未'}:
                        element = "火"
                    # ... other patterns
                    
                    half_desc = f"{''.join(unique_chars_list)}半会化{element}"
                    relationships.append({
                        'type': '地支半会',
                        'positions': unique_positions,
                        'characters': unique_chars_list,
                        'description': half_desc,
                        'points': 10
                    })
    
    return relationships

def mock_check_relationship(positions, chart, all_relationships):
    """Mock the check_relationship method"""
    # Sort positions for comparison
    positions = sorted(positions)
    
    # Get characters
    zhis = chart['zhis']
    num_pillars = len(zhis)
    
    selected_chars = []
    for pos in positions:
        if pos >= num_pillars:  # This is a zhi position
            selected_chars.append(zhis[pos - num_pillars])
        else:  # This is a gan position (shouldn't happen in this test)
            selected_chars.append("X")  # placeholder
    
    print(f"Check relationship for positions {positions}")
    print(f"Selected characters: {selected_chars}")
    
    # Find matching relationship
    for rel in all_relationships:
        print(f"  Comparing with: {rel['characters']} (positions {rel['positions']})")
        if sorted(rel['characters']) == sorted(selected_chars):
            print(f"  ✅ Character match found!")
            return rel
    
    print(f"  ❌ No match found")
    return None

def test_user_scenario():
    """Test the exact user scenario"""
    print("Testing User Scenario")
    print("=" * 50)
    
    # User's chart
    chart = {
        'zhis': ['巳', '巳', '申', '未']
    }
    
    print(f"Chart: {chart['zhis']}")
    print()
    
    # Step 1: Get all relationships
    all_relationships = mock_detect_all_relationships(chart)
    print(f"All relationships detected ({len(all_relationships)}):")
    for i, rel in enumerate(all_relationships):
        chars = ''.join(rel['characters'])
        print(f"  {i+1}. {rel['type']}: {chars} (pos {rel['positions']}) - {rel['description']}")
    print()
    
    # Step 2: Test clicking 巳申 (positions [4,6])
    print("Test 1: User clicks 巳申 (frontend sends [4,6])")
    result1 = mock_check_relationship([4, 6], chart, all_relationships)
    if result1:
        print(f"Result: ✅ {result1['type']} - {result1['description']}")
    else:
        print("Result: ❌ Not found")
    print()
    
    # Step 3: Test clicking 巳未 (positions [4,7])
    print("Test 2: User clicks 巳未 (frontend sends [4,7])")
    result2 = mock_check_relationship([4, 7], chart, all_relationships)
    if result2:
        print(f"Result: ✅ {result2['type']} - {result2['description']}")
    else:
        print("Result: ❌ Not found")
    print()

if __name__ == "__main__":
    test_user_scenario()