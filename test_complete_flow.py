#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test complete flow for relationship detection

import sys
sys.path.append('.')

from game_app import BaziGame

def test_complete_flow():
    """Test the complete flow with user's chart"""
    print("Testing Complete Flow: 巳巳申未")
    print("=" * 50)
    
    game = BaziGame()
    
    # Create chart matching user's scenario
    chart = {
        'gans': ['甲', '乙', '丙', '丁'],  # dummy gans
        'zhis': ['巳', '巳', '申', '未'],   # user's zhis
        'advanced_mode': False
    }
    
    game.current_chart = chart
    
    print("Chart setup:")
    print(f"  zhis: {chart['zhis']}")
    print()
    
    # Test 1: Detect all relationships first
    print("Step 1: Detect all relationships")
    all_relationships = game.detect_all_relationships(chart)
    
    print(f"Found {len(all_relationships)} total relationships:")
    for i, rel in enumerate(all_relationships):
        chars = ''.join(rel['characters'])
        print(f"  {i+1}. {rel['type']}: {chars} (positions {rel['positions']}) - {rel['description']}")
    print()
    
    # Test 2: Try to check specific relationships
    print("Step 2: Check specific relationships")
    
    # Test 巳申 (positions 0,2 in zhis → frontend sends 4,6)
    print("Testing 巳申 (frontend would send positions [4,6]):")
    frontend_positions = [4, 6]  # 0+4, 2+4
    result1 = game.check_relationship(frontend_positions)
    
    if result1:
        print(f"  ✅ Found: {result1['type']} - {result1['description']}")
    else:
        print(f"  ❌ NOT Found")
        
        # Debug: what characters were extracted?
        selected_chars = []
        for pos in frontend_positions:
            if pos >= 4:  # zhi position
                selected_chars.append(chart['zhis'][pos - 4])
            else:  # gan position
                selected_chars.append(chart['gans'][pos])
        print(f"     Extracted characters: {selected_chars}")
        
        # Debug: what relationships have matching characters?
        for rel in all_relationships:
            if sorted(rel['characters']) == sorted(selected_chars):
                print(f"     Match found in all_relationships: {rel}")
    print()
    
    # Test 巳未 (positions 0,3 in zhis → frontend sends 4,7)
    print("Testing 巳未 (frontend would send positions [4,7]):")
    frontend_positions = [4, 7]  # 0+4, 3+4
    result2 = game.check_relationship(frontend_positions)
    
    if result2:
        print(f"  ✅ Found: {result2['type']} - {result2['description']}")
    else:
        print(f"  ❌ NOT Found")
        
        # Debug: what characters were extracted?
        selected_chars = []
        for pos in frontend_positions:
            if pos >= 4:  # zhi position
                selected_chars.append(chart['zhis'][pos - 4])
            else:  # gan position
                selected_chars.append(chart['gans'][pos])
        print(f"     Extracted characters: {selected_chars}")
        
        # Debug: what relationships have matching characters?
        for rel in all_relationships:
            if sorted(rel['characters']) == sorted(selected_chars):
                print(f"     Match found in all_relationships: {rel}")
    print()

if __name__ == "__main__":
    test_complete_flow()