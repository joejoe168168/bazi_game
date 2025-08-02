#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bazi Interactive Relationship Game - Flask Backend
# Author: Based on existing Bazi codebase

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import datetime
from lunar_python import Solar, Lunar
from datas import *
from ganzhi import *
from common import *

app = Flask(__name__)
CORS(app)

class BaziGame:
    def __init__(self):
        self.current_chart = None
        self.found_relationships = []
        self.score = 0
        self.relationship_settings = {
            '天干五合': True,
            '天干相冲': True,
            '地支相冲': True,
            '地支六合': True,
            '地支相刑': True,
            '地支三合局': True,  # This controls both 三合 and 半合
            '地支三会方': True,  # This controls both 三会 and 半会
            '地支暗合': True,
            '地支相害': False,
            '地支相破': False
        }
        
    def generate_random_bazi(self, advanced_mode=False):
        """Generate a random Bazi chart for the game"""
        # Generate random date within reasonable range
        year = random.randint(1950, 2020)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Safe range for all months
        hour = random.randint(0, 23)
        is_female = random.choice([True, False])
        
        # Create lunar date
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        
        # Get Ganzhi for year, month, day, hour
        year_gz = lunar.getYearInGanZhi()
        month_gz = lunar.getMonthInGanZhi()
        day_gz = lunar.getDayInGanZhi()
        hour_gz = lunar.getTimeInGanZhi()
        
        # Extract individual characters
        chart = {
            'year_gan': year_gz[0],
            'year_zhi': year_gz[1],
            'month_gan': month_gz[0],
            'month_zhi': month_gz[1],
            'day_gan': day_gz[0],
            'day_zhi': day_gz[1],
            'hour_gan': hour_gz[0],
            'hour_zhi': hour_gz[1],
            'gans': [year_gz[0], month_gz[0], day_gz[0], hour_gz[0]],
            'zhis': [year_gz[1], month_gz[1], day_gz[1], hour_gz[1]],
            'date_info': f"{year}年{month}月{day}日{hour}时",
            'is_female': is_female,
            'advanced_mode': advanced_mode
        }
        
        if advanced_mode:
            # Calculate 大运 (Luck Pillars)
            dayun_gan, dayun_zhi = self.calculate_dayun(year_gz[0], month_gz, is_female)
            # Generate current 流年 (Year Pillar) - random current year
            current_year = random.randint(2020, 2024)
            current_solar = Solar.fromYmdHms(current_year, 1, 1, 0, 0, 0)
            current_lunar = current_solar.getLunar()
            liunian_gz = current_lunar.getYearInGanZhi()
            
            chart.update({
                'dayun_gan': dayun_gan,
                'dayun_zhi': dayun_zhi,
                'liunian_gan': liunian_gz[0],
                'liunian_zhi': liunian_gz[1],
                'gans': [year_gz[0], month_gz[0], day_gz[0], hour_gz[0], dayun_gan, liunian_gz[0]],
                'zhis': [year_gz[1], month_gz[1], day_gz[1], hour_gz[1], dayun_zhi, liunian_gz[1]],
                'current_year': current_year
            })
        
        self.current_chart = chart
        return chart
    
    def calculate_dayun(self, year_gan, month_gz, is_female):
        """Calculate current luck pillar (大运)"""
        # Direction based on year gan and gender
        gan_seq = Gan.index(year_gan)
        if is_female:
            direction = -1 if gan_seq % 2 == 0 else 1
        else:
            direction = 1 if gan_seq % 2 == 0 else -1
        
        # Get current luck pillar (simulate current age around 20-50)
        age_periods = random.randint(2, 6)  # 2-6 periods (each 10 years)
        
        gan_seq = Gan.index(month_gz[0])
        zhi_seq = Zhi.index(month_gz[1])
        
        for i in range(age_periods):
            gan_seq = (gan_seq + direction) % 10
            zhi_seq = (zhi_seq + direction) % 12
            
        return Gan[gan_seq], Zhi[zhi_seq]
    
    def detect_all_relationships(self, chart):
        """Detect all possible relationships in the chart"""
        relationships = []
        gans = chart['gans']
        zhis = chart['zhis']
        
        # Determine number of pillars based on mode
        num_pillars = 6 if chart.get('advanced_mode', False) else 4
        
        # Check Gan relationships (天干)
        for i in range(num_pillars):
            for j in range(i+1, num_pillars):
                gan1, gan2 = gans[i], gans[j]
                
                # Check 相合 (harmony) - 天干五合
                if self.relationship_settings['天干五合'] and ((gan1, gan2) in gan_hes or (gan2, gan1) in gan_hes):
                    rel_info = gan_hes.get((gan1, gan2), gan_hes.get((gan2, gan1)))
                    # Higher points for relationships involving 大运/流年
                    points = 15 if (i >= 4 or j >= 4) and num_pillars == 6 else 10
                    
                    # Extract the element from the description (e.g., "化土" -> "合土")
                    element = ""
                    if "化土" in rel_info:
                        element = "合土"
                    elif "化金" in rel_info:
                        element = "合金"
                    elif "化水" in rel_info:
                        element = "合水"
                    elif "化木" in rel_info:
                        element = "合木"
                    elif "化火" in rel_info:
                        element = "合火"
                    
                    short_desc = f"{gan1}{gan2}{element}" if element else f"{gan1}{gan2}相合"
                    
                    relationships.append({
                        'type': '天干五合',
                        'positions': [i, j],
                        'characters': [gan1, gan2],
                        'description': short_desc,
                        'full_description': rel_info,
                        'points': points
                    })
                
                # Check 相冲 (conflict) - 天干相冲
                if self.relationship_settings['天干相冲'] and ((gan1, gan2) in gan_chongs or (gan2, gan1) in gan_chongs):
                    # Higher points for relationships involving 大运/流年
                    points = 12 if (i >= 4 or j >= 4) and num_pillars == 6 else 8
                    relationships.append({
                        'type': '天干相冲',
                        'positions': [i, j],
                        'characters': [gan1, gan2],
                        'description': "天干相冲，主冲突不和",
                        'points': points
                    })
        
        # Check Zhi relationships (地支)
        for i in range(num_pillars):
            for j in range(i+1, num_pillars):
                zhi1, zhi2 = zhis[i], zhis[j]
                
                # Check 六合 (six harmonies)
                if self.relationship_settings['地支六合'] and zhi_atts[zhi1]['六'] == zhi2:
                    # Higher points for relationships involving 大运/流年
                    points = 18 if (i >= 4 or j >= 4) and num_pillars == 6 else 12
                    
                    # Get the resulting element from zhi_6hes
                    pair_key = f"{zhi1}{zhi2}"
                    reverse_key = f"{zhi2}{zhi1}"
                    element = zhi_6hes.get(pair_key, zhi_6hes.get(reverse_key, ""))
                    
                    desc = f"{zhi1}{zhi2}六合化{element}" if element else f"{zhi1}{zhi2}六合"
                    
                    relationships.append({
                        'type': '地支六合',
                        'positions': [i, j],
                        'characters': [zhi1, zhi2],
                        'description': desc,
                        'points': points
                    })
                
                # Check 相冲 (conflict)
                if self.relationship_settings['地支相冲'] and zhi_atts[zhi1]['冲'] == zhi2:
                    # Higher points for relationships involving 大运/流年
                    points = 15 if (i >= 4 or j >= 4) and num_pillars == 6 else 10
                    relationships.append({
                        'type': '地支相冲',
                        'positions': [i, j],
                        'characters': [zhi1, zhi2],
                        'description': "地支相冲，主动荡变化",
                        'points': points
                    })
                
                # Check 相刑 (punishment)
                if self.relationship_settings['地支相刑'] and zhi_atts[zhi1]['刑'] == zhi2:
                    # Higher points for relationships involving 大运/流年
                    points = 20 if (i >= 4 or j >= 4) and num_pillars == 6 else 15
                    relationships.append({
                        'type': '地支相刑',
                        'positions': [i, j],
                        'characters': [zhi1, zhi2],
                        'description': "地支相刑，主刑伤阻滞",
                        'points': points
                    })
                
                # Check 相害 (harm)
                if self.relationship_settings['地支相害'] and zhi_atts[zhi1]['害'] == zhi2:
                    # Higher points for relationships involving 大运/流年
                    points = 18 if (i >= 4 or j >= 4) and num_pillars == 6 else 12
                    relationships.append({
                        'type': '地支相害',
                        'positions': [i, j],
                        'characters': [zhi1, zhi2],
                        'description': "地支相害，主暗中损害",
                        'points': points
                    })
                
                # Check 相破 (destruction)
                if self.relationship_settings['地支相破'] and zhi_atts[zhi1]['破'] == zhi2:
                    # Higher points for relationships involving 大运/流年
                    points = 15 if (i >= 4 or j >= 4) and num_pillars == 6 else 10
                    relationships.append({
                        'type': '地支相破',
                        'positions': [i, j],
                        'characters': [zhi1, zhi2],
                        'description': "地支相破，主破坏损失",
                        'points': points
                    })
        
        # Check 三合 (triple harmonies) - supports both full and partial patterns
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
                
                # Only proceed if we have at least 2 positions
                if len(positions) >= 2:
                    # Get the actual characters at these positions
                    chars = [zhis[i] for i in positions]
                    unique_chars = list(set(chars))  # Remove duplicates
                    
                    # Only create relationships with unique characters
                    if len(unique_chars) == len(chars):  # No duplicates
                        # Full 三合 pattern (3 unique characters)
                        if len(positions) == 3:
                            points = 30 if any(i >= 4 for i in positions) and num_pillars == 6 else 20
                            relationships.append({
                                'type': '地支三合',
                                'positions': positions,
                                'characters': chars,
                                'description': desc,
                                'points': points
                            })
                        
                        # Partial 三合 pattern (半合 - 2 unique characters)
                        elif len(positions) == 2:
                            points = 18 if any(i >= 4 for i in positions) and num_pillars == 6 else 12
                            
                            # Get the element for this pattern
                            element = ""
                            if set(pattern) == {'申', '子', '辰'}:
                                element = "水"
                            elif set(pattern) == {'寅', '午', '戌'}:
                                element = "火" 
                            elif set(pattern) == {'巳', '酉', '丑'}:
                                element = "金"
                            elif set(pattern) == {'亥', '卯', '未'}:
                                element = "木"
                            
                            # Use zhi_half_3hes data if available for specific pairs
                            pair_tuple = tuple(sorted(chars))
                            half_info = zhi_half_3hes.get(pair_tuple, zhi_half_3hes.get(tuple(reversed(pair_tuple)), ""))
                            
                            if half_info:
                                half_desc = f"{''.join(chars)}半合 {half_info}"
                            else:
                                half_desc = f"{''.join(chars)}半合化{element}"
                            
                            relationships.append({
                                'type': '地支半合',
                                'positions': positions,
                                'characters': chars,
                                'description': half_desc,
                                'points': points
                            })
                    # If we have duplicates but multiple positions, we need different logic
                    elif len(positions) > len(unique_chars):
                        # For cases like 午戌午 - treat as 半合 with unique characters only
                        if len(unique_chars) == 2:
                            # Find positions of the unique characters
                            unique_positions = []
                            seen_chars = set()
                            for i in positions:
                                char = zhis[i]
                                if char not in seen_chars:
                                    unique_positions.append(i)
                                    seen_chars.add(char) 
                            
                            if len(unique_positions) == 2:
                                points = 18 if any(i >= 4 for i in unique_positions) and num_pillars == 6 else 12
                                unique_chars_list = [zhis[i] for i in unique_positions]
                                
                                # Get the element for this pattern
                                element = ""
                                if set(pattern) == {'申', '子', '辰'}:
                                    element = "水"
                                elif set(pattern) == {'寅', '午', '戌'}:
                                    element = "火" 
                                elif set(pattern) == {'巳', '酉', '丑'}:
                                    element = "金"
                                elif set(pattern) == {'亥', '卯', '未'}:
                                    element = "木"
                                
                                # Use zhi_half_3hes data if available for specific pairs
                                pair_tuple = tuple(sorted(unique_chars_list))
                                half_info = zhi_half_3hes.get(pair_tuple, zhi_half_3hes.get(tuple(reversed(pair_tuple)), ""))
                                
                                if half_info:
                                    half_desc = f"{''.join(unique_chars_list)}半合 {half_info}"
                                else:
                                    half_desc = f"{''.join(unique_chars_list)}半合化{element}"
                                
                                relationships.append({
                                    'type': '地支半合',
                                    'positions': unique_positions,
                                    'characters': unique_chars_list,
                                    'description': half_desc,
                                    'points': points
                                })
        
        # Check 三会 (triple meetings) - supports both full and partial patterns
        if self.relationship_settings['地支三会方']:
            sanhui_patterns = [
                (['亥', '子', '丑'], '亥子丑三会水方'),
                (['寅', '卯', '辰'], '寅卯辰三会木方'),
                (['巳', '午', '未'], '巳午未三会火方'),
                (['申', '酉', '戌'], '申酉戌三会金方')
            ]
            
            for pattern, desc in sanhui_patterns:
                positions = []
                for i, zhi in enumerate(zhis[:num_pillars]):
                    if zhi in pattern:
                        positions.append(i)
                
                # Only proceed if we have at least 2 positions
                if len(positions) >= 2:
                    # Get the actual characters at these positions
                    chars = [zhis[i] for i in positions]
                    unique_chars = list(set(chars))  # Remove duplicates
                    
                    # Only create relationships with unique characters
                    if len(unique_chars) == len(chars):  # No duplicates
                        # Full 三会 pattern (3 unique characters)
                        if len(positions) == 3:
                            points = 27 if any(i >= 4 for i in positions) and num_pillars == 6 else 18
                            relationships.append({
                                'type': '地支三会',
                                'positions': positions,
                                'characters': chars,
                                'description': desc,
                                'points': points
                            })
                        
                        # Partial 三会 pattern (半会 - 2 unique characters)
                        elif len(positions) == 2:
                            points = 15 if any(i >= 4 for i in positions) and num_pillars == 6 else 10
                            
                            # Get the element for this pattern
                            element = ""
                            if set(pattern) == {'亥', '子', '丑'}:
                                element = "水"
                            elif set(pattern) == {'寅', '卯', '辰'}:
                                element = "木" 
                            elif set(pattern) == {'巳', '午', '未'}:
                                element = "火"
                            elif set(pattern) == {'申', '酉', '戌'}:
                                element = "金"
                            
                            half_desc = f"{''.join(chars)}半会化{element}"
                            
                            relationships.append({
                                'type': '地支半会',
                                'positions': positions,
                                'characters': chars,
                                'description': half_desc,
                                'points': points
                            })
                    # If we have duplicates but multiple positions, we need different logic
                    elif len(positions) > len(unique_chars):
                        # For cases like 午午未 - treat as 半会 with unique characters only
                        if len(unique_chars) == 2:
                            # Find positions of the unique characters
                            unique_positions = []
                            seen_chars = set()
                            for i in positions:
                                char = zhis[i]
                                if char not in seen_chars:
                                    unique_positions.append(i)
                                    seen_chars.add(char) 
                            
                            if len(unique_positions) == 2:
                                points = 15 if any(i >= 4 for i in unique_positions) and num_pillars == 6 else 10
                                unique_chars_list = [zhis[i] for i in unique_positions]
                                
                                # Get the element for this pattern
                                element = ""
                                if set(pattern) == {'亥', '子', '丑'}:
                                    element = "水"
                                elif set(pattern) == {'寅', '卯', '辰'}:
                                    element = "木" 
                                elif set(pattern) == {'巳', '午', '未'}:
                                    element = "火"
                                elif set(pattern) == {'申', '酉', '戌'}:
                                    element = "金"
                                
                                half_desc = f"{''.join(unique_chars_list)}半会化{element}"
                                
                                relationships.append({
                                    'type': '地支半会',
                                    'positions': unique_positions,
                                    'characters': unique_chars_list,
                                    'description': half_desc,
                                    'points': points
                                })
        
        return relationships
    
    def check_relationship(self, positions):
        """Check if selected positions form a valid relationship"""
        if not self.current_chart:
            return None
            
        all_relationships = self.detect_all_relationships(self.current_chart)
        
        # Sort positions for comparison
        positions = sorted(positions)
        
        # Get the actual characters at these positions
        gans = self.current_chart['gans']
        zhis = self.current_chart['zhis']
        num_pillars = 6 if self.current_chart.get('advanced_mode', False) else 4
        
        selected_chars = []
        for pos in positions:
            if pos >= num_pillars:  # This is a zhi position
                selected_chars.append(zhis[pos - num_pillars])
            else:  # This is a gan position
                selected_chars.append(gans[pos])
        
        # Find a matching relationship based on characters, not just positions
        for rel in all_relationships:
            if sorted(rel['characters']) == sorted(selected_chars):
                # Check if this exact combination of positions hasn't been found yet
                rel_id = f"{rel['type']}_{sorted(positions)}"
                found_ids = [f"{r['type']}_{sorted(r.get('actual_positions', r['positions']))}" for r in self.found_relationships]
                
                if rel_id not in found_ids:
                    # Create a new relationship object with actual positions
                    new_rel = rel.copy()
                    new_rel['actual_positions'] = positions
                    self.found_relationships.append(new_rel)
                    self.score += rel['points']
                    return new_rel
        
        return None

# Global game instance
game = BaziGame()

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Start a new game with a random Bazi chart"""
    global game
    data = request.json or {}
    advanced_mode = data.get('advanced_mode', False)
    
    game = BaziGame()  # Reset game state
    chart = game.generate_random_bazi(advanced_mode)
    all_relationships = game.detect_all_relationships(chart)
    
    # Calculate hint counts
    hint_counts = {}
    for rel in all_relationships:
        rel_type = rel['type']
        hint_counts[rel_type] = hint_counts.get(rel_type, 0) + 1
    
    return jsonify({
        'chart': chart,
        'hint_counts': hint_counts,
        'total_relationships': len(all_relationships),
        'score': game.score
    })

@app.route('/api/check_relationship', methods=['POST'])
def check_relationship():
    """Check if selected positions form a valid relationship"""
    data = request.json
    positions = data.get('positions', [])
    
    if len(positions) < 2 or len(positions) > 3:
        return jsonify({'error': 'Invalid number of positions selected'}), 400
    
    # Frontend sends positions in this format:
    # - Gan positions: 0, 1, 2, 3 (for 4-pillar) or 0, 1, 2, 3, 4, 5 (for 6-pillar)
    # - Zhi positions: num_pillars+0, num_pillars+1, num_pillars+2, etc.
    # We need to pass them directly to check_relationship which handles the conversion
    relationship = game.check_relationship(positions)
    
    if relationship:
        # Calculate remaining relationships
        all_relationships = game.detect_all_relationships(game.current_chart)
        remaining = len(all_relationships) - len(game.found_relationships)
        
        return jsonify({
            'found': True,
            'relationship': relationship,
            'score': game.score,
            'remaining_relationships': remaining,
            'game_complete': remaining == 0
        })
    else:
        return jsonify({
            'found': False,
            'score': game.score
        })

@app.route('/api/get_hints', methods=['GET'])
def get_hints():
    """Get hint counts for current chart"""
    if not game.current_chart:
        return jsonify({'error': 'No active game'}), 400
    
    all_relationships = game.detect_all_relationships(game.current_chart)
    found_ids = [f"{r['type']}_{r['positions']}" for r in game.found_relationships]
    
    remaining_relationships = [
        rel for rel in all_relationships 
        if f"{rel['type']}_{rel['positions']}" not in found_ids
    ]
    
    hint_counts = {}
    for rel in remaining_relationships:
        rel_type = rel['type']
        hint_counts[rel_type] = hint_counts.get(rel_type, 0) + 1
    
    return jsonify({
        'hint_counts': hint_counts,
        'total_remaining': len(remaining_relationships)
    })

@app.route('/api/game_status', methods=['GET'])
def game_status():
    """Get current game status"""
    if not game.current_chart:
        return jsonify({'error': 'No active game'}), 400
    
    all_relationships = game.detect_all_relationships(game.current_chart)
    remaining = len(all_relationships) - len(game.found_relationships)
    
    return jsonify({
        'score': game.score,
        'found_relationships': len(game.found_relationships),
        'total_relationships': len(all_relationships),
        'remaining_relationships': remaining,
        'game_complete': remaining == 0,
        'chart': game.current_chart
    })

@app.route('/api/show_all_relationships', methods=['GET'])
def show_all_relationships():
    """Show all relationships in the current chart"""
    if not game.current_chart:
        return jsonify({'error': 'No active game'}), 400
    
    all_relationships = game.detect_all_relationships(game.current_chart)
    found_ids = [f"{r['type']}_{sorted(r.get('actual_positions', r['positions']))}" for r in game.found_relationships]
    
    # Separate found and unfound relationships
    found_rels = []
    unfound_rels = []
    
    for rel in all_relationships:
        rel_id = f"{rel['type']}_{sorted(rel['positions'])}"
        if rel_id in found_ids:
            # Find the corresponding found relationship to get actual positions
            for found_rel in game.found_relationships:
                found_id = f"{found_rel['type']}_{sorted(found_rel.get('actual_positions', found_rel['positions']))}"
                if found_id == rel_id:
                    found_rels.append(found_rel)
                    break
        else:
            unfound_rels.append(rel)
    
    return jsonify({
        'all_relationships': all_relationships,
        'found_relationships': found_rels,
        'unfound_relationships': unfound_rels,
        'total_count': len(all_relationships),
        'found_count': len(found_rels),
        'unfound_count': len(unfound_rels)
    })

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get current relationship settings"""
    return jsonify({
        'relationship_settings': game.relationship_settings
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update relationship settings"""
    data = request.json
    new_settings = data.get('relationship_settings', {})
    
    # Validate settings keys
    valid_keys = set(game.relationship_settings.keys())
    invalid_keys = set(new_settings.keys()) - valid_keys
    
    if invalid_keys:
        return jsonify({'error': f'Invalid setting keys: {list(invalid_keys)}'}), 400
    
    # Update settings
    for key, value in new_settings.items():
        if isinstance(value, bool):
            game.relationship_settings[key] = value
        else:
            return jsonify({'error': f'Setting {key} must be a boolean value'}), 400
    
    return jsonify({
        'success': True,
        'relationship_settings': game.relationship_settings,
        'message': 'Settings updated successfully'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)