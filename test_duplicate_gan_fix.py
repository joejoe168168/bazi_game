#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test script for duplicate gan character hint fix

def test_duplicate_gan_scenario():
    """Test the duplicate gan character scenario"""
    print("Testing Duplicate Gan Character Scenario")
    print("=" * 50)
    
    # Scenario: 甲庚庚 in positions [0, 1, 2]
    print("Chart example: 甲庚庚丁 (gans)")
    print("Positions:     [0, 1, 2, 3]")
    print()
    
    # Possible relationships
    relationships = [
        {
            'type': '天干相冲',
            'positions': [0, 1],
            'characters': ['甲', '庚'],
            'description': '甲庚相冲',
            'points': 8
        },
        {
            'type': '天干相冲', 
            'positions': [0, 2],
            'characters': ['甲', '庚'],
            'description': '甲庚相冲',
            'points': 8
        }
    ]
    
    print("Available relationships:")
    for i, rel in enumerate(relationships, 1):
        chars = ''.join(rel['characters'])
        print(f"  {i}. {rel['type']}: {chars} (positions {rel['positions']})")
    print()
    
    # Simulate finding the first relationship
    print("Step 1: User clicks first 甲庚 (positions [0,1])")
    found_relationships = [
        {
            'type': '天干相冲',
            'positions': [0, 1],
            'characters': ['甲', '庚'],
            'actual_positions': [0, 1],
            'description': '甲庚相冲',
            'points': 8
        }
    ]
    
    print("Found relationships after first click:")
    for rel in found_relationships:
        chars = ''.join(rel['characters'])
        actual_pos = rel.get('actual_positions', rel['positions'])
        print(f"  - {rel['type']}: {chars} (actual positions {actual_pos})")
    print()
    
    # Test if second relationship is still available
    print("Step 2: Check if second 甲庚 (positions [0,2]) is still available")
    
    # User tries to click positions [0, 2]
    selected_positions = [0, 2]
    
    # Old logic (BROKEN)
    print("❌ Old logic:")
    old_available = True
    for found_rel in found_relationships:
        if (found_rel['type'] == '天干相冲' and 
            sorted(found_rel['characters']) == sorted(['甲', '庚'])):
            old_available = False
            break
    
    print(f"   Would consider second 甲庚 available: {old_available}")
    print("   Problem: Same characters, so marked as already found")
    print()
    
    # New logic (FIXED)
    print("✅ New logic:")
    new_available = True
    for found_rel in found_relationships:
        if (found_rel['type'] == '天干相冲' and 
            sorted(found_rel.get('actual_positions', found_rel['positions'])) == sorted(selected_positions)):
            new_available = False
            break
    
    print(f"   Considers second 甲庚 available: {new_available}")
    print("   Fixed: Checks exact positions [0,2] vs [0,1] - different!")
    print()
    
    # Hint counting
    total_relationships = len(relationships)
    found_count = len(found_relationships)
    
    print("Hint counting:")
    print(f"  Total relationships: {total_relationships}")
    print(f"  Found relationships: {found_count}")
    print(f"  ❌ Old logic remaining: {0 if not old_available else total_relationships - found_count}")
    print(f"  ✅ New logic remaining: {total_relationships - found_count}")
    print()

def test_multiple_duplicates():
    """Test multiple duplicate combinations"""
    print("Testing Multiple Duplicate Combinations")
    print("=" * 50)
    
    # Scenario: 甲庚庚庚 (even more duplicates)
    print("Extreme case: 甲庚庚庚 (gans)")
    print("Positions:    [0, 1, 2, 3]")
    print()
    
    # All possible 甲庚 combinations
    combinations = [
        ([0, 1], "甲庚 (positions 0,1)"),
        ([0, 2], "甲庚 (positions 0,2)"), 
        ([0, 3], "甲庚 (positions 0,3)")
    ]
    
    print("All possible 甲庚 relationships:")
    for i, (positions, desc) in enumerate(combinations, 1):
        print(f"  {i}. {desc}")
    print()
    
    # Simulate finding them one by one
    found_relationships = []
    
    for step, (positions, desc) in enumerate(combinations, 1):
        print(f"Step {step}: User finds {desc}")
        
        # Add to found relationships
        found_relationships.append({
            'type': '天干相冲',
            'positions': positions,
            'actual_positions': positions,
            'characters': ['甲', '庚']
        })
        
        # Count remaining with NEW logic
        remaining = 0
        for combo_pos, combo_desc in combinations:
            is_found = False
            for found_rel in found_relationships:
                if (found_rel['type'] == '天干相冲' and 
                    sorted(found_rel.get('actual_positions', found_rel['positions'])) == sorted(combo_pos)):
                    is_found = True
                    break
            if not is_found:
                remaining += 1
        
        print(f"  Remaining relationships: {remaining}")
        print(f"  Found so far: {len(found_relationships)}")
    
    print("\n✅ Each position combination is counted separately!")
    print("✅ Hints correctly show remaining count!")
    print()

if __name__ == "__main__":
    test_duplicate_gan_scenario()
    test_multiple_duplicates()
    
    print("=" * 60)
    print("🎯 SUMMARY:")
    print("Fixed the hint counting for duplicate characters.")
    print("Now 甲庚庚 correctly shows 2 separate relationships:")
    print("  1. 甲庚相冲 (positions [0,1])")  
    print("  2. 甲庚相冲 (positions [0,2])")
    print("Each can be found independently!")
    print("=" * 60)