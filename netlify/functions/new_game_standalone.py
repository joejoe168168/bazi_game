import json
import random
from datetime import datetime, timedelta

def handler(event, context):
    """
    Standalone new game function with all dependencies inline
    """
    # Handle CORS preflight requests
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    
    try:
        # Get request body
        params = json.loads(event.get('body', '{}'))
        advanced_mode = params.get('advanced_mode', False)
        custom_settings = params.get('settings', {})
        
        # Default settings
        DEFAULT_SETTINGS = {
            '天干五合': True, '天干相冲': True,
            '地支相冲': True, '地支六合': True,
            '地支相刑': False, '地支三合局': True,
            '地支三会方': True, '地支暗合': True,
            '地支相害': False, '地支相破': False
        }
        
        # Merge custom settings with defaults
        settings = DEFAULT_SETTINGS.copy()
        settings.update(custom_settings)
        
        # Basic data
        gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        zhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # Generate random chart
        num_pillars = 6 if advanced_mode else 4
        chart_gans = [random.choice(gans) for _ in range(num_pillars)]
        chart_zhis = [random.choice(zhis) for _ in range(num_pillars)]
        
        chart = {
            'year_gan': chart_gans[0],
            'year_zhi': chart_zhis[0],
            'month_gan': chart_gans[1],
            'month_zhi': chart_zhis[1],
            'day_gan': chart_gans[2],
            'day_zhi': chart_zhis[2],
            'hour_gan': chart_gans[3],
            'hour_zhi': chart_zhis[3],
            'gans': chart_gans,
            'zhis': chart_zhis,
            'date_info': f'随机八字 {chart_gans[0]}{chart_zhis[0]} {chart_gans[1]}{chart_zhis[1]} {chart_gans[2]}{chart_zhis[2]} {chart_gans[3]}{chart_zhis[3]}',
            'advanced_mode': advanced_mode
        }
        
        if advanced_mode:
            chart.update({
                'dayun_gan': chart_gans[4],
                'dayun_zhi': chart_zhis[4],
                'liunian_gan': chart_gans[5],
                'liunian_zhi': chart_zhis[5],
                'current_year': 2024
            })
        
        # Simple relationship detection
        all_relationships = []
        
        # Basic 天干相合 detection
        if settings.get('天干五合', True):
            gan_hes = {('甲', '己'): '合土', ('乙', '庚'): '合金', ('丙', '辛'): '合水', ('丁', '壬'): '合木', ('戊', '癸'): '合火'}
            for i in range(len(chart_gans)):
                for j in range(i + 1, len(chart_gans)):
                    pair = tuple(sorted([chart_gans[i], chart_gans[j]]))
                    if pair in gan_hes:
                        all_relationships.append({
                            'type': '天干相合',
                            'positions': [i, j],
                            'characters': [chart_gans[i], chart_gans[j]],
                            'description': f"{chart_gans[i]}{chart_gans[j]}{gan_hes[pair]}",
                            'points': 10
                        })
        
        # Basic 地支六合 detection  
        if settings.get('地支六合', True):
            zhi_hes = {('子', '丑'): '合土', ('寅', '亥'): '合木', ('卯', '戌'): '合火', ('辰', '酉'): '合金', ('巳', '申'): '合水', ('午', '未'): '合土'}
            for i in range(len(chart_zhis)):
                for j in range(i + 1, len(chart_zhis)):
                    pair = tuple(sorted([chart_zhis[i], chart_zhis[j]]))
                    if pair in zhi_hes:
                        all_relationships.append({
                            'type': '地支六合',
                            'positions': [i + num_pillars, j + num_pillars],
                            'characters': [chart_zhis[i], chart_zhis[j]],
                            'description': f"{chart_zhis[i]}{chart_zhis[j]}{zhi_hes[pair]}",
                            'points': 8
                        })
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'chart': chart,
                'all_relationships': all_relationships
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({'error': str(e)})
        }