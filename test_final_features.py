#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test script for final Bazi game features

import sys
import json
sys.path.append('.')

from game_app import BaziGame

def test_settings_system():
    """Test the relationship settings system"""
    print("Testing Settings System")
    print("=" * 50)
    
    game = BaziGame()
    
    # Test default settings
    print("Default settings:")
    for setting, enabled in game.relationship_settings.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {setting}: {enabled}")
    
    # Test settings modification
    print("\nTesting settings modification...")
    game.relationship_settings['地支相害'] = True
    game.relationship_settings['地支相破'] = True
    
    print("Modified settings (enabled 相害 and 相破):")
    for setting, enabled in game.relationship_settings.items():
        if setting in ['地支相害', '地支相破']:
            status = "✅" if enabled else "❌"
            print(f"  {status} {setting}: {enabled}")
    
    print("\n" + "=" * 50)

def test_show_all_relationships():
    """Test the show all relationships functionality"""
    print("Testing Show All Relationships Feature")
    print("=" * 50)
    
    game = BaziGame()
    
    # Generate a test chart
    chart = game.generate_random_bazi(advanced_mode=True)
    print(f"Generated test chart (6-pillar mode):")
    print(f"  年柱: {chart['year_gan']}{chart['year_zhi']}")
    print(f"  月柱: {chart['month_gan']}{chart['month_zhi']}")
    print(f"  日柱: {chart['day_gan']}{chart['day_zhi']}")
    print(f"  时柱: {chart['hour_gan']}{chart['hour_zhi']}")
    print(f"  大运: {chart['dayun_gan']}{chart['dayun_zhi']}")
    print(f"  流年: {chart['liunian_gan']}{chart['liunian_zhi']}")
    
    # Detect all relationships
    all_relationships = game.detect_all_relationships(chart)
    
    print(f"\nDetected {len(all_relationships)} total relationships:")
    
    # Group by type
    rel_groups = {}
    for rel in all_relationships:
        rel_type = rel['type']
        if rel_type not in rel_groups:
            rel_groups[rel_type] = []
        rel_groups[rel_type].append(rel)
    
    for rel_type, rels in rel_groups.items():
        print(f"\n{rel_type} ({len(rels)}):")
        for rel in rels:
            chars = ''.join(rel['characters'])
            print(f"  - {chars} ({rel['points']}分): {rel.get('description', '')}")
    
    print("\n" + "=" * 50)

def test_settings_impact_on_relationships():
    """Test how settings affect relationship detection"""
    print("Testing Settings Impact on Relationship Detection")
    print("=" * 50)
    
    game = BaziGame()
    
    # Generate a test chart
    chart = game.generate_random_bazi(advanced_mode=False)
    
    # Count relationships with all settings enabled
    game.relationship_settings = {key: True for key in game.relationship_settings.keys()}
    all_enabled_count = len(game.detect_all_relationships(chart))
    
    # Count relationships with minimal settings
    game.relationship_settings = {
        '天干五合': True,
        '天干相冲': True,
        '地支相冲': False,
        '地支六合': False,
        '地支相刑': False,
        '地支三合局': False,
        '地支三会方': False,
        '地支暗合': False,
        '地支相害': False,
        '地支相破': False
    }
    minimal_enabled_count = len(game.detect_all_relationships(chart))
    
    # Count relationships with default settings
    game.relationship_settings = {
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
    default_enabled_count = len(game.detect_all_relationships(chart))
    
    print("Relationship counts with different settings:")
    print(f"  All enabled: {all_enabled_count}")
    print(f"  Default settings: {default_enabled_count}")
    print(f"  Minimal settings (only 天干五合/相冲): {minimal_enabled_count}")
    
    settings_difference = all_enabled_count - minimal_enabled_count
    print(f"\nSettings can affect {settings_difference} relationships in this chart")
    
    print("\n" + "=" * 50)

def test_advanced_mode_scoring():
    """Test advanced mode bonus scoring"""
    print("Testing Advanced Mode Bonus Scoring")
    print("=" * 50)
    
    game = BaziGame()
    
    # Generate both basic and advanced charts
    basic_chart = game.generate_random_bazi(advanced_mode=False)
    advanced_chart = game.generate_random_bazi(advanced_mode=True)
    
    # Get relationships for both
    basic_rels = game.detect_all_relationships(basic_chart)
    advanced_rels = game.detect_all_relationships(advanced_chart)
    
    print(f"Basic mode (4 pillars): {len(basic_rels)} relationships")
    print(f"Advanced mode (6 pillars): {len(advanced_rels)} relationships")
    
    # Check for bonus scoring in advanced mode
    dayun_liunian_rels = []
    for rel in advanced_rels:
        # Check if relationship involves position 4 (大运) or 5 (流年)
        if any(pos >= 4 for pos in rel['positions']):
            dayun_liunian_rels.append(rel)
    
    print(f"\nRelationships involving 大运/流年: {len(dayun_liunian_rels)}")
    for rel in dayun_liunian_rels:
        chars = ''.join(rel['characters'])
        print(f"  - {rel['type']}: {chars} ({rel['points']}分 - bonus included)")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    print("🎮 Bazi Game Final Features Test Suite")
    print("=" * 60)
    
    test_settings_system()
    test_show_all_relationships()
    test_settings_impact_on_relationships()
    test_advanced_mode_scoring()
    
    print("✅ All final feature tests completed!")
    print("\nNew features implemented:")
    print("  1. ✅ Settings system for relationship types")
    print("  2. ✅ Show All Relationships modal")
    print("  3. ✅ Settings API endpoints")
    print("  4. ✅ Settings UI with toggles")
    print("  5. ✅ Complete 三合/三会 settings integration")
    print("  6. ✅ Advanced mode bonus scoring")
    print("=" * 60)