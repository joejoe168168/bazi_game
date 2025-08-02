#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test script for user's specific chart: 巳巳申未

import sys
sys.path.append('.')

from datas import *
from ganzhi import *
from common import *

class TestUserChart:
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
    
    def detect_all_relationships(self, chart):
        """Test relationship detection with user's chart"""
        relationships = []
        zhis = chart['zhis']
        num_pillars = len(zhis)
        
        print(f"Chart zhis: {zhis}")
        print(f"Number of pillars: {num_pillars}")
        print()
        
        # Check Zhi relationships (地支)
        for i in range(num_pillars):
            for j in range(i+1, num_pillars):
                zhi1, zhi2 = zhis[i], zhis[j]
                print(f"Checking positions {i} and {j}: {zhi1} vs {zhi2}")
                
                # Check 六合 (six harmonies)
                if self.relationship_settings['地支六合']:
                    if zhi_atts[zhi1]['六'] == zhi2:
                        print(f"  ✅ Found 六合: {zhi1}{zhi2} (zhi_atts[{zhi1}]['六'] = {zhi_atts[zhi1]['六']})")
                        
                        # Get the resulting element from zhi_6hes
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
                    else:
                        print(f"  ❌ No 六合: {zhi1}{zhi2} (zhi_atts[{zhi1}]['六'] = {zhi_atts[zhi1]['六']}, not {zhi2})")
                
                # Check 相冲 (conflict)
                if self.relationship_settings['地支相冲']:
                    if zhi_atts[zhi1]['冲'] == zhi2:
                        print(f"  ✅ Found 相冲: {zhi1}{zhi2}")
                        relationships.append({
                            'type': '地支相冲',
                            'positions': [i, j],
                            'characters': [zhi1, zhi2],
                            'description': f"{zhi1}{zhi2}相冲",
                            'points': 10
                        })
                
                print()
        
        # Check 三会 patterns
        if self.relationship_settings['地支三会方']:
            print("Checking 三会 patterns...")
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
                
                print(f"Pattern {pattern}: found positions {positions}")
                
                # Only proceed if we have at least 2 positions
                if len(positions) >= 2:
                    # Get the actual characters at these positions
                    chars = [zhis[i] for i in positions]
                    unique_chars = list(set(chars))  # Remove duplicates
                    
                    print(f"  Characters: {chars}, Unique: {unique_chars}")
                    
                    # Only create relationships with unique characters
                    if len(unique_chars) == len(chars):  # No duplicates
                        # Partial 三会 pattern (半会 - 2 unique characters)
                        if len(positions) == 2:
                            points = 10
                            element = ""
                            if set(pattern) == {'亥', '子', '丑'}:
                                element = "水"
                            elif set(pattern) == {'寅', '卯', '辰'}:
                                element = "木" 
                            elif set(pattern) == {'巳', '午', '未'}:
                                element = "火"
                            elif set(pattern) == {'申', '酉', '戌'}:
                                element = "金"
                            
                            half_desc = f"{''.join(chars)}半会化{element}"
                            print(f"  ✅ Found 半会: {half_desc}")
                            
                            relationships.append({
                                'type': '地支半会',
                                'positions': positions,
                                'characters': chars,
                                'description': half_desc,
                                'points': points
                            })
                    # If we have duplicates but multiple positions
                    elif len(positions) > len(unique_chars):
                        print(f"  Handling duplicates...")
                        # For cases like 巳巳未 - treat as 半会 with unique characters only
                        if len(unique_chars) == 2:
                            # Find positions of the unique characters
                            unique_positions = []
                            seen_chars = set()
                            for i in positions:
                                char = zhis[i]
                                if char not in seen_chars:
                                    unique_positions.append(i)
                                    seen_chars.add(char) 
                            
                            if len(unique_positions) == 2:
                                points = 10
                                unique_chars_list = [zhis[i] for i in unique_positions]
                                element = ""
                                if set(pattern) == {'亥', '子', '丑'}:
                                    element = "水"
                                elif set(pattern) == {'寅', '卯', '辰'}:
                                    element = "木" 
                                elif set(pattern) == {'巳', '午', '未'}:
                                    element = "火"
                                elif set(pattern) == {'申', '酉', '戌'}:
                                    element = "金"
                                
                                half_desc = f"{''.join(unique_chars_list)}半会化{element}"
                                print(f"  ✅ Found unique 半会: {half_desc}")
                                
                                relationships.append({
                                    'type': '地支半会',
                                    'positions': unique_positions,
                                    'characters': unique_chars_list,
                                    'description': half_desc,
                                    'points': points
                                })
                
                print()
        
        return relationships

def test_user_specific_chart():
    """Test the user's specific chart: 巳巳申未"""
    print("Testing User's Specific Chart: 巳巳申未")
    print("=" * 60)
    
    test = TestUserChart()
    
    # User's chart
    chart = {
        'zhis': ['巳', '巳', '申', '未'],
        'advanced_mode': False
    }
    
    relationships = test.detect_all_relationships(chart)
    
    print("=" * 60)
    print("DETECTED RELATIONSHIPS:")
    print("=" * 60)
    
    if relationships:
        for rel in relationships:
            chars = ''.join(rel['characters'])
            print(f"{rel['type']}: {chars}")
            print(f"  描述: {rel['description']}")
            print(f"  位置: {rel['positions']}")
            print(f"  分数: +{rel['points']}")
            print()
    else:
        print("❌ No relationships detected!")
    
    print("Expected relationships:")
    print("  1. 巳申六合化水 (positions 0,2 or 1,2)")
    print("     - Because zhi_atts['巳']['六'] = '申'")
    print("  2. 巳未半会化火 (positions 0,3 or 1,3)")  
    print("     - Because 巳未 are part of 巳午未三会火方")

if __name__ == "__main__":
    test_user_specific_chart()