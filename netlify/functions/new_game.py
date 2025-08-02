# netlify/functions/new_game.py
# -*- coding: utf-8 -*-
import json
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from bazi_utils import generate_random_bazi, detect_all_relationships

# Default relationship settings
DEFAULT_SETTINGS = {
    '天干五合': True, '天干相冲': True,
    '地支相冲': True, '地支六合': True,
    '地支相刑': False, '地支三合局': True,
    '地支三会方': True, '地支暗合': True,
    '地支相害': False, '地支相破': False
}

def handler(event, context):
    """
    Netlify Function handler for starting a new game.
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
        
        # Merge custom settings with defaults
        settings = DEFAULT_SETTINGS.copy()
        settings.update(custom_settings)
        
        # Generate a new Bazi chart
        chart = generate_random_bazi(advanced_mode)
        
        # Detect all possible relationships in the new chart with merged settings
        all_relationships = detect_all_relationships(chart, settings)
        
        # Prepare the response payload
        payload = {
            'chart': chart,
            'all_relationships': all_relationships
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*', # CORS header for development
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps(payload, ensure_ascii=False)
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
