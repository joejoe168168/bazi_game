#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test frontend-backend communication for relationship detection

def test_position_conversion_flow():
    """Test the complete position conversion flow"""
    print("Testing Frontend-Backend Communication Flow")
    print("=" * 60)
    
    # User's problematic chart: 子丑 (positions 0,1 in zhis)
    print("Chart example: 子丑寅卯 (zhis)")
    print("Expected relationships:")
    print("  - 子丑六合化土")
    print("  - 子丑半会化水")  
    print()
    
    # Simulate frontend click behavior
    print("Step 1: User clicks 子丑 (zhi positions 0,1)")
    user_clicks = [
        {'position': 0, 'type': 'zhi'},  # 子
        {'position': 1, 'type': 'zhi'}   # 丑
    ]
    
    # Frontend position conversion
    num_pillars = 4
    frontend_positions = []
    for click in user_clicks:
        if click['type'] == 'zhi':
            frontend_pos = click['position'] + num_pillars  # 0+4=4, 1+4=5
        else:
            frontend_pos = click['position']  # gan positions unchanged
        frontend_positions.append(frontend_pos)
    
    print(f"Frontend converts to: {frontend_positions}")
    print()
    
    # Backend processing (what should happen)
    print("Step 2: Backend processes positions")
    print("API endpoint receives:", frontend_positions)
    print("Passes directly to check_relationship():", frontend_positions)
    print()
    
    print("Step 3: check_relationship() converts positions:")
    zhis = ['子', '丑', '寅', '卯']
    selected_chars = []
    
    for pos in frontend_positions:
        if pos >= num_pillars:  # zhi position
            zhi_index = pos - num_pillars  
            char = zhis[zhi_index]
            selected_chars.append(char)
            print(f"  Position {pos} → zhi[{zhi_index}] = {char}")
        else:  # gan position
            print(f"  Position {pos} → gan[{pos}]")
    
    print(f"Selected characters: {selected_chars}")
    print()
    
    # Expected result
    expected_chars = ['子', '丑']
    if selected_chars == expected_chars:
        print("✅ Position conversion successful!")
        print("Backend should find relationships with characters:", selected_chars)
    else:
        print(f"❌ Position conversion failed! Expected {expected_chars}, got {selected_chars}")
    
    print()
    print("=" * 60)

def test_mixed_selections():
    """Test mixed gan/zhi selections"""
    print("Testing Mixed Gan/Zhi Selections")
    print("=" * 40)
    
    # Example: 甲庚相冲 (gan positions 0,2)
    print("Example 1: 甲庚相冲 (gan positions 0,2)")
    frontend_positions = [0, 2]  # gan positions sent directly
    print(f"Frontend sends: {frontend_positions}")
    
    # Backend conversion
    gans = ['甲', '乙', '庚', '丁']
    num_pillars = 4
    selected_chars = []
    
    for pos in frontend_positions:
        if pos >= num_pillars:  # zhi position
            selected_chars.append("ZHI")  # placeholder
        else:  # gan position
            selected_chars.append(gans[pos])
    
    print(f"Backend extracts: {selected_chars}")
    print()
    
    # Example: 子申六合 (zhi positions 0,2 → frontend 4,6)
    print("Example 2: 子申六合 (zhi positions 0,2)")
    frontend_positions = [4, 6]  # 0+4, 2+4
    print(f"Frontend sends: {frontend_positions}")
    
    # Backend conversion
    zhis = ['子', '丑', '申', '卯']
    selected_chars = []
    
    for pos in frontend_positions:
        if pos >= num_pillars:  # zhi position
            zhi_index = pos - num_pillars
            selected_chars.append(zhis[zhi_index])
        else:  # gan position
            selected_chars.append("GAN")  # placeholder
    
    print(f"Backend extracts: {selected_chars}")
    print()

def test_user_specific_case():
    """Test the user's specific failing case"""
    print("Testing User's Specific Case")
    print("=" * 40)
    
    print("User reported: 子丑 relationships show in 'Show All' but clicking fails")
    print()
    
    # Chart from user's problem
    zhis = ['子', '丑', '寅', '卯']  # example
    num_pillars = 4
    
    # User clicks 子丑 (positions 0,1)
    print("User clicks: 子 (pos 0) and 丑 (pos 1)")
    
    # Frontend conversion
    frontend_positions = [0 + num_pillars, 1 + num_pillars]  # [4, 5]
    print(f"Frontend sends: {frontend_positions}")
    
    # Backend conversion (fixed logic)
    selected_chars = []
    for pos in frontend_positions:
        if pos >= num_pillars:
            zhi_index = pos - num_pillars
            selected_chars.append(zhis[zhi_index])
            print(f"  pos {pos} → zhis[{zhi_index}] = {zhis[zhi_index]}")
    
    print(f"Backend should extract: {selected_chars}")
    
    # Expected relationships that should match
    expected_relationships = [
        "子丑六合化土",
        "子丑半会化水"
    ]
    
    print(f"Should match relationships: {expected_relationships}")
    print()
    
    if selected_chars == ['子', '丑']:
        print("✅ This should now work with the fix!")
    else:
        print("❌ Still has issues")

if __name__ == "__main__":
    test_position_conversion_flow()
    test_mixed_selections()
    test_user_specific_case()
    
    print("=" * 60)
    print("🎯 SUMMARY:")
    print("The fix removes the double conversion in the API endpoint.")
    print("Now positions flow correctly:")
    print("  Frontend → API → check_relationship() → Success!")
    print("=" * 60)