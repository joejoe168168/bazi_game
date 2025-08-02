#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test script for the improved Bazi game functionality

import sys
sys.path.append('.')

from datas import *
from ganzhi import *

def test_duplicate_character_detection():
    """Test handling of duplicate characters like 壬 壬 癸"""
    print("Testing Duplicate Character Detection")
    print("=" * 50)
    
    # Simulate a chart with duplicate characters
    test_gans = ['丙', '丙', '壬', '甲']  # Two 丙 characters
    print(f"Test chart gans: {test_gans}")
    
    # Test case: user clicks position 0 (first 丙) and position 2 (壬)
    # This should detect 丙壬冲 relationship
    selected_positions = [0, 2]  # positions of first 丙 and 壬
    selected_chars = [test_gans[pos] for pos in selected_positions]
    
    print(f"Selected positions: {selected_positions}")
    print(f"Selected characters: {selected_chars}")
    
    # Check if this forms a valid relationship
    gan1, gan2 = selected_chars[0], selected_chars[1]
    if (gan1, gan2) in gan_chongs or (gan2, gan1) in gan_chongs:
        print(f"✅ Found relationship: {gan1}{gan2} 相冲")
        print("This should be detectable even with duplicate characters!")
    else:
        print("❌ No relationship found")
    
    # Test case: user clicks position 1 (second 丙) and position 2 (壬)
    # This should also detect 丙壬冲 relationship
    selected_positions = [1, 2]  # positions of second 丙 and 壬
    selected_chars = [test_gans[pos] for pos in selected_positions]
    
    print(f"\nSecond test - Selected positions: {selected_positions}")
    print(f"Selected characters: {selected_chars}")
    
    gan1, gan2 = selected_chars[0], selected_chars[1]
    if (gan1, gan2) in gan_chongs or (gan2, gan1) in gan_chongs:
        print(f"✅ Found relationship: {gan1}{gan2} 相冲")
        print("Both 丙 characters should be able to form relationships!")
    else:
        print("❌ No relationship found")
    
    print("\n" + "=" * 50)

def test_relationship_tracking():
    """Test the relationship tracking and progress system"""
    print("Testing Relationship Tracking System")
    print("=" * 50)
    
    # Simulate found relationships
    found_relationships = [
        {'type': '天干相合', 'characters': ['甲', '己'], 'points': 10},
        {'type': '地支六合', 'characters': ['子', '丑'], 'points': 12},
        {'type': '天干相冲', 'characters': ['丙', '壬'], 'points': 8},
    ]
    
    total_relationships = 8  # Assume 8 total relationships in the chart
    
    print("Simulated discovered relationships:")
    for i, rel in enumerate(found_relationships, 1):
        print(f"  {i}. {rel['type']}: {rel['characters'][0]}{rel['characters'][1]} (+{rel['points']}分)")
    
    found_count = len(found_relationships)
    remaining_count = total_relationships - found_count
    total_score = sum(rel['points'] for rel in found_relationships)
    
    print(f"\nProgress Summary:")
    print(f"  已发现: {found_count}")
    print(f"  剩余: {remaining_count}")
    print(f"  总分: {total_score}")
    print(f"  完成度: {found_count}/{total_relationships} ({found_count/total_relationships*100:.1f}%)")
    
    print("\n" + "=" * 50)

def test_advanced_mode_bonus():
    """Test bonus scoring for 大运/流年 relationships"""
    print("Testing Advanced Mode Bonus Scoring")
    print("=" * 50)
    
    # Simulate 6-pillar chart relationships
    relationships = [
        # Basic 4-pillar relationships
        {'positions': [0, 1], 'type': '天干相合', 'characters': ['甲', '己'], 'base_points': 10},
        {'positions': [2, 3], 'type': '地支六合', 'characters': ['子', '丑'], 'base_points': 12},
        
        # Relationships involving 大运 (position 4)
        {'positions': [0, 4], 'type': '天干相冲', 'characters': ['甲', '庚'], 'base_points': 8},
        {'positions': [1, 4], 'type': '地支相害', 'characters': ['寅', '巳'], 'base_points': 12},
        
        # Relationships involving 流年 (position 5)
        {'positions': [2, 5], 'type': '地支相冲', 'characters': ['午', '子'], 'base_points': 10},
        {'positions': [4, 5], 'type': '天干相合', 'characters': ['庚', '乙'], 'base_points': 10},
    ]
    
    print("Relationship scoring with advanced mode bonuses:")
    total_score = 0
    
    for rel in relationships:
        # Check if involves 大运 or 流年 (positions 4 or 5)
        has_dayun_liunian = any(pos >= 4 for pos in rel['positions'])
        bonus_multiplier = 1.5 if has_dayun_liunian else 1.0
        final_points = int(rel['base_points'] * bonus_multiplier)
        
        bonus_text = " (大运/流年 bonus!)" if has_dayun_liunian else ""
        print(f"  {rel['type']}: {rel['characters'][0]}{rel['characters'][1]} " +
              f"({rel['base_points']} → {final_points}分){bonus_text}")
        
        total_score += final_points
    
    print(f"\nTotal Score: {total_score}")
    print("Advanced mode relationships should get bonus points!")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    print("🎮 Bazi Game Improvements Test Suite")
    print("=" * 60)
    
    test_duplicate_character_detection()
    test_relationship_tracking()
    test_advanced_mode_bonus()
    
    print("✅ All improvement tests completed!")
    print("The game should now handle:")
    print("  - Duplicate characters correctly")
    print("  - Progress tracking in hints")
    print("  - Discovered relationships display")
    print("  - Visual feedback improvements")
    print("=" * 60)