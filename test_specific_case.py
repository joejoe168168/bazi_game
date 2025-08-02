#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test the specific case mentioned by the user

class MockGame:
    def __init__(self):
        self.relationship_settings = {'地支三合局': True}
    
    def detect_partial_sanhe(self, zhis, num_pillars=4):
        """Test the partial 三合 detection logic"""
        relationships = []
        
        if self.relationship_settings['地支三合局']:
            sanhe_patterns = [
                (['申', '子', '辰'], '申子辰三合水局'),
                (['寅', '午', '戌'], '寅午戌三合火局'),
                (['巳', '酉', '丑'], '巳酉丑三合金局'),
                (['亥', '卯', '未'], '亥卯未三合木局')
            ]
            
            for pattern, desc in sanhe_patterns:
                positions = []
                for i, zhi in enumerate(zhis[:num_pillars]):
                    if zhi in pattern:
                        positions.append(i)
                
                # Full 三合 pattern (3 characters)
                if len(positions) == 3:
                    points = 20
                    relationships.append({
                        'type': '地支三合',
                        'positions': positions,
                        'characters': [zhis[i] for i in positions],
                        'description': desc,
                        'points': points
                    })
                
                # Partial 三合 pattern (半合 - 2 characters)  
                elif len(positions) == 2:
                    points = 12
                    chars = [zhis[i] for i in positions]
                    half_desc = f"{''.join(chars)}半合({desc.split('三合')[1]})"
                    relationships.append({
                        'type': '地支半合',
                        'positions': positions,
                        'characters': chars,
                        'description': half_desc,
                        'points': points
                    })
        
        return relationships

def test_specific_cases():
    print("Testing Specific User Cases")
    print("=" * 50)
    
    game = MockGame()
    
    # Case 1: 丑巳巳 (user's original example)
    print("Case 1: 丑巳巳")
    zhis1 = ['丑', '巳', '巳', '戌']
    rels1 = game.detect_partial_sanhe(zhis1)
    for rel in rels1:
        chars = ''.join(rel['characters'])
        print(f"  {rel['type']}: {chars} - {rel['description']}")
    
    print()
    
    # Case 2: Just 丑巳 (2 characters only)
    print("Case 2: 丑巳 (only 2 characters)")
    zhis2 = ['丑', '巳', '午', '戌']  # Only 丑 and 巳, no third member
    rels2 = game.detect_partial_sanhe(zhis2)
    for rel in rels2:
        chars = ''.join(rel['characters'])
        print(f"  {rel['type']}: {chars} - {rel['description']}")
    
    print()
    
    # Case 3: 巳酉 (another partial)
    print("Case 3: 巳酉 (partial)")
    zhis3 = ['巳', '酉', '午', '戌']
    rels3 = game.detect_partial_sanhe(zhis3)
    for rel in rels3:
        chars = ''.join(rel['characters'])
        print(f"  {rel['type']}: {chars} - {rel['description']}")
    
    print()
    
    # Case 4: 酉丑 (another partial)
    print("Case 4: 酉丑 (partial)")
    zhis4 = ['酉', '丑', '午', '戌']
    rels4 = game.detect_partial_sanhe(zhis4)
    for rel in rels4:
        chars = ''.join(rel['characters'])
        print(f"  {rel['type']}: {chars} - {rel['description']}")
    
    print("\n" + "=" * 50)
    print("Summary:")
    print("- 丑巳巳: Detected as full 三合 (because 3 positions match pattern)")
    print("- 丑巳: Detected as 半合 (2 characters from 巳酉丑 pattern)")
    print("- 巳酉: Detected as 半合 (2 characters from 巳酉丑 pattern)")
    print("- 酉丑: Detected as 半合 (2 characters from 巳酉丑 pattern)")

if __name__ == "__main__":
    test_specific_cases()