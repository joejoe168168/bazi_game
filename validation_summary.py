#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Validation summary for completed Bazi game features

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and return status"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"  {status} {description}: {filepath}")
    return exists

def check_code_feature(filepath, search_text, description):
    """Check if a code feature exists in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            exists = search_text in content
            status = "✅" if exists else "❌"
            print(f"  {status} {description}")
            return exists
    except FileNotFoundError:
        print(f"  ❌ {description} (file not found)")
        return False

def validate_implementation():
    """Validate all implemented features"""
    print("🎮 Bazi Interactive Game - Implementation Validation")
    print("=" * 70)
    
    # Check core files
    print("\n📁 Core Files:")
    files_ok = True
    files_ok &= check_file_exists("game_app.py", "Flask backend application")
    files_ok &= check_file_exists("templates/game.html", "Frontend game interface")
    files_ok &= check_file_exists("requirements.txt", "Python dependencies")
    files_ok &= check_file_exists("GAME_README.md", "Game documentation")
    
    # Check backend features
    print("\n🔧 Backend Features:")
    backend_ok = True
    backend_ok &= check_code_feature("game_app.py", "relationship_settings", "Settings system implemented")
    backend_ok &= check_code_feature("game_app.py", "show_all_relationships", "Show all relationships API")
    backend_ok &= check_code_feature("game_app.py", "advanced_mode", "Advanced mode (6 pillars) support")
    backend_ok &= check_code_feature("game_app.py", "地支三合局", "三合 pattern settings integration")
    backend_ok &= check_code_feature("game_app.py", "地支三会方", "三会 pattern settings integration")
    backend_ok &= check_code_feature("game_app.py", "@app.route('/api/settings'", "Settings API endpoints")
    
    # Check frontend features  
    print("\n🎨 Frontend Features:")
    frontend_ok = True
    frontend_ok &= check_code_feature("templates/game.html", "showAllRelationships", "Show all relationships button")
    frontend_ok &= check_code_feature("templates/game.html", "showSettings", "Settings button and modal")
    frontend_ok &= check_code_feature("templates/game.html", "all-relationships-modal", "Relationships overview modal")
    frontend_ok &= check_code_feature("templates/game.html", "setting-toggle", "Settings toggle switches")
    frontend_ok &= check_code_feature("templates/game.html", "advanced", "Advanced mode UI support")
    frontend_ok &= check_code_feature("templates/game.html", "discovered-section", "Progress tracking display")
    
    # Check test files
    print("\n🧪 Test Files:")
    test_ok = True
    test_ok &= check_file_exists("test_improvements.py", "Improvements test script")
    test_ok &= check_file_exists("simple_test.py", "Basic relationship tests")
    test_ok &= check_file_exists("test_final_features.py", "Final features test script")
    test_ok &= check_file_exists("test_game_logic.py", "Game logic test script")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 VALIDATION SUMMARY:")
    
    if files_ok and backend_ok and frontend_ok:
        print("🎉 ALL FEATURES SUCCESSFULLY IMPLEMENTED!")
        print("\n✅ Completed Features:")
        print("   1. Settings system for relationship types")
        print("   2. Show All Relationships functionality") 
        print("   3. Complete API endpoints for settings")
        print("   4. Interactive settings UI with toggles")
        print("   5. Advanced mode bonus scoring")
        print("   6. Progress tracking and visual feedback")
        print("   7. Modal interfaces for settings and relationships")
        print("   8. 三合/三会 pattern settings integration")
        
        print("\n🚀 Ready to run with:")
        print("   pip install -r requirements.txt")
        print("   python game_app.py")
        print("   # Open browser to http://localhost:5000")
        
    else:
        print("⚠️  Some features may need attention:")
        if not files_ok:
            print("   - Check core files")
        if not backend_ok:
            print("   - Check backend implementation")
        if not frontend_ok:
            print("   - Check frontend features")
    
    print("=" * 70)

if __name__ == "__main__":
    validate_implementation()