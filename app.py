#!/usr/bin/env python3
"""
Local Flask server for testing the Bazi game locally
Run this to test locally before deploying to Netlify
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import sys
import os

# Add netlify functions to path
netlify_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'netlify', 'functions')
sys.path.insert(0, netlify_path)

# Import netlify functions
from bazi_utils import generate_random_bazi, detect_all_relationships

app = Flask(__name__)
CORS(app)

# Default settings (matching netlify function)
DEFAULT_SETTINGS = {
    '天干五合': True, '天干相冲': True,
    '地支相冲': True, '地支六合': True,
    '地支相刑': False, '地支三合局': True,
    '地支三会方': True, '地支暗合': True,
    '地支相害': False, '地支相破': False
}

@app.route('/')
def index():
    """Serve the main game page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Start a new game - local version of netlify function"""
    try:
        data = request.get_json() or {}
        advanced_mode = data.get('advanced_mode', False)
        custom_settings = data.get('settings', {})
        
        # Merge custom settings with defaults
        settings = DEFAULT_SETTINGS.copy()
        settings.update(custom_settings)
        
        # Generate a new Bazi chart
        chart = generate_random_bazi(advanced_mode)
        
        # Detect all possible relationships
        all_relationships = detect_all_relationships(chart, settings)
        
        return jsonify({
            'chart': chart,
            'all_relationships': all_relationships
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check_relationship', methods=['POST'])
def check_relationship():
    """Check a relationship - local version of netlify function"""
    try:
        data = request.get_json() or {}
        positions = data.get('positions', [])
        chart = data.get('chart')
        all_relationships = data.get('all_relationships', [])
        found_relationships = data.get('found_relationships', [])
        
        # Basic validation
        if not all([chart, positions]):
            return jsonify({'error': 'Missing required data: chart and positions.'}), 400
        
        if len(positions) < 2 or len(positions) > 3:
            return jsonify({'error': 'Invalid number of positions selected'}), 400

        # Normalize positions for comparison
        sorted_positions = sorted(positions)
        
        # Check if this exact combination of positions has already been found
        for rel in found_relationships:
            if sorted(rel.get('actual_positions', [])) == sorted_positions:
                return jsonify({'found': False, 'message': 'This relationship has already been found.'})

        # Find a matching relationship from the pre-calculated list
        found_match = None
        for rel in all_relationships:
            # We must match the characters because positions might differ if zhis are duplicated
            selected_chars = []
            num_pillars = 6 if chart.get('advanced_mode') else 4
            gans = chart.get('gans', [])
            zhis = chart.get('zhis', [])

            for pos in sorted_positions:
                if pos >= num_pillars: # This is a zhi position
                    selected_chars.append(zhis[pos - num_pillars])
                else: # This is a gan position
                    selected_chars.append(gans[pos])

            # Check if the selected characters match the relationship's characters
            if sorted(rel['characters']) == sorted(selected_chars):
                # Check if this EXACT combination of positions has been found before
                # For duplicates like 甲庚庚, [0,1] and [0,2] are different relationships
                is_already_found = False
                for found_rel in found_relationships:
                    if (found_rel['type'] == rel['type'] and 
                        sorted(found_rel.get('actual_positions', found_rel['positions'])) == sorted_positions):
                        is_already_found = True
                        break
                
                if not is_already_found:
                    found_match = rel
                    break

        if found_match:
            # Add the actual positions from user selection to the found relationship
            response_rel = found_match.copy()
            response_rel['actual_positions'] = sorted_positions

            return jsonify({'found': True, 'relationship': response_rel})
        else:
            return jsonify({'found': False, 'message': 'No valid relationship found for the selection.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎮 Starting Bazi Game Local Server")
    print("📍 Open http://localhost:5000 to play the game")
    print("🔧 This is for local testing before Netlify deployment")
    app.run(debug=True, port=5000)