#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test script for Bazi game logic

import sys
import os
sys.path.append('.')

# Mock the missing modules for testing
class MockSolar:
    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def fromYmdHms(cls, year, month, day, hour, minute, second):
        return cls(year, month, day, hour, minute, second)
    
    def getLunar(self):
        return MockLunar()

class MockLunar:
    def getYearInGanZhi(self):
        return "甲", "子"
    
    def getMonthInGanZhi(self):
        return "丙", "寅"
    
    def getDayInGanZhi(self):
        return "戊", "辰"
    
    def getTimeInGanZhi(self):
        return "庚", "午"

# Patch the imports
sys.modules['lunar_python'] = type(sys)('lunar_python')
sys.modules['lunar_python'].Solar = MockSolar
sys.modules['flask'] = type(sys)('flask')
sys.modules['flask_cors'] = type(sys)('flask_cors')

# Mock Flask functions
class MockFlask:
    def __init__(self, name):
        pass
    def route(self, path, methods=None):
        def decorator(f):
            return f
        return decorator
    def run(self, **kwargs):
        pass

def jsonify(data):
    return data

sys.modules['flask'].Flask = MockFlask
sys.modules['flask'].jsonify = jsonify
sys.modules['flask'].request = type('Request', (), {'json': {}})()
sys.modules['flask'].render_template = lambda x: x
sys.modules['flask_cors'].CORS = lambda x: None

# Now test our game logic
from game_app import BaziGame

def test_basic_mode():
    print("Testing Basic Mode (4 pillars)...")
    game = BaziGame()
    chart = game.generate_random_bazi(advanced_mode=False)
    
    print(f"Generated chart: {chart['gans']} {chart['zhis']}")
    print(f"Advanced mode: {chart.get('advanced_mode', False)}")
    
    relationships = game.detect_all_relationships(chart)
    print(f"Found {len(relationships)} relationships:")
    
    for rel in relationships:
        print(f"  - {rel['type']}: {rel['characters']} (positions: {rel['positions']}, points: {rel['points']})")
    
    return len(relationships)

def test_advanced_mode():
    print("\nTesting Advanced Mode (6 pillars)...")
    game = BaziGame()
    chart = game.generate_random_bazi(advanced_mode=True)
    
    print(f"Generated chart: {chart['gans']} {chart['zhis']}")
    print(f"Advanced mode: {chart.get('advanced_mode', False)}")
    if chart.get('advanced_mode'):
        print(f"大运: {chart['dayun_gan']}{chart['dayun_zhi']}")
        print(f"流年: {chart['current_year']}年{chart['liunian_gan']}{chart['liunian_zhi']}")
    
    relationships = game.detect_all_relationships(chart)
    print(f"Found {len(relationships)} relationships:")
    
    for rel in relationships:
        print(f"  - {rel['type']}: {rel['characters']} (positions: {rel['positions']}, points: {rel['points']})")
    
    return len(relationships)

def test_relationship_checking():
    print("\nTesting Relationship Checking...")
    game = BaziGame()
    
    # Create a test chart with known relationships
    chart = {
        'year_gan': '甲', 'year_zhi': '子',
        'month_gan': '己', 'month_zhi': '丑',  # 甲己合，子丑合
        'day_gan': '丙', 'day_zhi': '午',
        'hour_gan': '壬', 'hour_zhi': '子',   # 丙壬冲，子午冲
        'gans': ['甲', '己', '丙', '壬'],
        'zhis': ['子', '丑', '午', '子'],
        'advanced_mode': False
    }
    
    game.current_chart = chart
    relationships = game.detect_all_relationships(chart)
    
    print("Test chart relationships:")
    for rel in relationships:
        print(f"  - {rel['type']}: {rel['characters']} (positions: {rel['positions']})")
    
    # Test checking a relationship
    result = game.check_relationship([0, 1])  # Should find 甲己合
    if result:
        print(f"Successfully found: {result['type']} - {result['characters']}")
    else:
        print("No relationship found at positions [0, 1]")

if __name__ == "__main__":
    print("=" * 60)
    print("Bazi Interactive Game - Test Suite")
    print("=" * 60)
    
    basic_rels = test_basic_mode()
    advanced_rels = test_advanced_mode()
    test_relationship_checking()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"Basic mode typically finds: {basic_rels} relationships")
    print(f"Advanced mode typically finds: {advanced_rels} relationships")
    print("Advanced mode should generally find more relationships due to 6 pillars")
    print("=" * 60)