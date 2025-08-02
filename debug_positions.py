#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Debug position conversion issue

def test_position_conversion():
    """Test the position conversion logic"""
    print("Position Conversion Debug")
    print("=" * 40)
    
    # User's chart: 巳巳申未
    zhis = ['巳', '巳', '申', '未']
    num_pillars = 4
    
    print(f"Chart zhis: {zhis}")
    print(f"Positions:  [0,   1,   2,   3]")
    print()
    
    # Simulate user clicking 巳申
    print("User clicks: First 巳 (pos 0) and 申 (pos 2)")
    
    # Frontend position conversion (what gets sent to backend)
    frontend_positions = []
    for pos in [0, 2]:  # User clicked zhi positions 0 and 2
        frontend_pos = pos + num_pillars  # zhi positions are offset by num_pillars
        frontend_positions.append(frontend_pos)
    
    print(f"Frontend sends: {frontend_positions}")
    
    # Backend position conversion (what backend extracts)
    selected_chars = []
    for pos in frontend_positions:
        if pos >= num_pillars:  # This is a zhi position
            zhi_index = pos - num_pillars
            char = zhis[zhi_index]
            selected_chars.append(char)
            print(f"  pos {pos} → zhi[{zhi_index}] = {char}")
        else:  # This is a gan position  
            print(f"  pos {pos} → gan[{pos}]")
    
    print(f"Backend extracts: {selected_chars}")
    print()
    
    # Check if this matches what we expect
    expected = ['巳', '申']
    if selected_chars == expected:
        print("✅ Position conversion working correctly!")
    else:
        print(f"❌ Position conversion error! Expected {expected}, got {selected_chars}")
    
    print()
    print("=" * 40)

def test_all_conversions():
    """Test all position conversions for the user's chart"""
    print("All Possible Position Conversions")
    print("=" * 40)
    
    zhis = ['巳', '巳', '申', '未']
    num_pillars = 4
    
    print(f"Chart: {zhis}")
    print()
    
    # All possible pairs
    pairs = [
        ([0, 1], ['巳', '巳']),
        ([0, 2], ['巳', '申']),
        ([0, 3], ['巳', '未']),
        ([1, 2], ['巳', '申']),
        ([1, 3], ['巳', '未']),
        ([2, 3], ['申', '未'])
    ]
    
    for positions, expected_chars in pairs:
        # Convert to frontend positions
        frontend_pos = [pos + num_pillars for pos in positions]
        
        # Convert back in backend
        backend_chars = []
        for pos in frontend_pos:
            if pos >= num_pillars:
                backend_chars.append(zhis[pos - num_pillars])
        
        match = "✅" if backend_chars == expected_chars else "❌"
        print(f"{match} Positions {positions} → Frontend {frontend_pos} → Backend {backend_chars}")

if __name__ == "__main__":
    test_position_conversion()
    test_all_conversions()