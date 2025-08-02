import json
import random

def handler(event, context):
    """Simple new game function without complex imports"""
    try:
        # Simple test chart without complex dependencies
        gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        zhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        chart = {
            'year_gan': random.choice(gans),
            'year_zhi': random.choice(zhis),
            'month_gan': random.choice(gans),
            'month_zhi': random.choice(zhis),
            'day_gan': random.choice(gans),
            'day_zhi': random.choice(zhis),
            'hour_gan': random.choice(gans),
            'hour_zhi': random.choice(zhis),
            'gans': [random.choice(gans) for _ in range(4)],
            'zhis': [random.choice(zhis) for _ in range(4)],
            'date_info': '测试八字',
            'advanced_mode': False
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'chart': chart,
                'all_relationships': []  # Empty for now
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