# netlify/functions/bazi_utils.py
# -*- coding: utf-8 -*-
import random
from datas import *
from ganzhi import *
from common import *
from lunar_python import Solar, Lunar

# Standalone, stateless utility functions for Bazi calculations.

def calculate_dayun(year_gan, month_gz, is_female):
    """Calculate current luck pillar (大运)"""
    gan_seq_year = Gan.index(year_gan)
    if is_female:
        direction = -1 if gan_seq_year % 2 == 0 else 1
    else:
        direction = 1 if gan_seq_year % 2 == 0 else -1
    
    age_periods = random.randint(2, 6)
    
    gan_seq_month = Gan.index(month_gz[0])
    zhi_seq_month = Zhi.index(month_gz[1])
    
    for _ in range(age_periods):
        gan_seq_month = (gan_seq_month + direction) % 10
        zhi_seq_month = (zhi_seq_month + direction) % 12
        
    return Gan[gan_seq_month], Zhi[zhi_seq_month]

def generate_random_bazi(advanced_mode=False):
    """Generate a random Bazi chart for the game"""
    year = random.randint(1950, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    is_female = random.choice([True, False])
    
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    
    year_gz = lunar.getYearInGanZhi()
    month_gz = lunar.getMonthInGanZhi()
    day_gz = lunar.getDayInGanZhi()
    hour_gz = lunar.getTimeInGanZhi()
    
    chart = {
        'year_gan': year_gz[0], 'year_zhi': year_gz[1],
        'month_gan': month_gz[0], 'month_zhi': month_gz[1],
        'day_gan': day_gz[0], 'day_zhi': day_gz[1],
        'hour_gan': hour_gz[0], 'hour_zhi': hour_gz[1],
        'gans': [year_gz[0], month_gz[0], day_gz[0], hour_gz[0]],
        'zhis': [year_gz[1], month_gz[1], day_gz[1], hour_gz[1]],
        'date_info': f"{year}年{month}月{day}日{hour}时",
        'is_female': is_female,
        'advanced_mode': advanced_mode
    }
    
    if advanced_mode:
        dayun_gan, dayun_zhi = calculate_dayun(year_gz[0], month_gz, is_female)
        current_year = random.randint(2020, 2024)
        current_solar = Solar.fromYmdHms(current_year, 1, 1, 0, 0, 0)
        liunian_gz = current_solar.getLunar().getYearInGanZhi()
        
        chart.update({
            'dayun_gan': dayun_gan, 'dayun_zhi': dayun_zhi,
            'liunian_gan': liunian_gz[0], 'liunian_zhi': liunian_gz[1],
            'gans': chart['gans'] + [dayun_gan, liunian_gz[0]],
            'zhis': chart['zhis'] + [dayun_zhi, liunian_gz[1]],
            'current_year': current_year
        })
    
    return chart

def detect_all_relationships(chart, relationship_settings):
    """Detect all possible relationships in the chart"""
    relationships = []
    gans = chart['gans']
    zhis = chart['zhis']
    num_pillars = 6 if chart.get('advanced_mode', False) else 4
    
    # Check Gan relationships (天干)
    for i in range(num_pillars):
        for j in range(i+1, num_pillars):
            gan1, gan2 = gans[i], gans[j]
            
            if relationship_settings.get('天干五合', True) and ((gan1, gan2) in gan_hes or (gan2, gan1) in gan_hes):
                rel_info = gan_hes.get((gan1, gan2), gan_hes.get((gan2, gan1)))
                points = 15 if (i >= 4 or j >= 4) and num_pillars == 6 else 10
                element = "".join(c for c in rel_info if c in "土金水木火")
                short_desc = f"{gan1}{gan2}合化{element}" if element else f"{gan1}{gan2}相合"
                relationships.append({'type': '天干五合','positions': [i, j],'characters': [gan1, gan2],'description': short_desc,'full_description': rel_info,'points': points})
            
            if relationship_settings.get('天干相冲', True) and ((gan1, gan2) in gan_chongs or (gan2, gan1) in gan_chongs):
                points = 12 if (i >= 4 or j >= 4) and num_pillars == 6 else 8
                relationships.append({'type': '天干相冲','positions': [i, j],'characters': [gan1, gan2],'description': "天干相冲，主冲突不和",'points': points})

    # Check Zhi relationships (地支)
    for i in range(num_pillars):
        for j in range(i+1, num_pillars):
            zhi1, zhi2 = zhis[i], zhis[j]
            
            if relationship_settings.get('地支六合', True) and zhi_atts[zhi1]['六'] == zhi2:
                points = 18 if (i >= 4 or j >= 4) and num_pillars == 6 else 12
                pair_key, reverse_key = f"{zhi1}{zhi2}", f"{zhi2}{zhi1}"
                element = zhi_6hes.get(pair_key, zhi_6hes.get(reverse_key, ""))
                desc = f"{zhi1}{zhi2}六合化{element}" if element else f"{zhi1}{zhi2}六合"
                relationships.append({'type': '地支六合','positions': [i, j],'characters': [zhi1, zhi2],'description': desc,'points': points})

            if relationship_settings.get('地支相冲', True) and zhi_atts[zhi1]['冲'] == zhi2:
                points = 15 if (i >= 4 or j >= 4) and num_pillars == 6 else 10
                relationships.append({'type': '地支相冲','positions': [i, j],'characters': [zhi1, zhi2],'description': "地支相冲，主动荡变化",'points': points})

            if relationship_settings.get('地支相刑', True) and zhi_atts[zhi1]['刑'] == zhi2:
                points = 20 if (i >= 4 or j >= 4) and num_pillars == 6 else 15
                relationships.append({'type': '地支相刑','positions': [i, j],'characters': [zhi1, zhi2],'description': "地支相刑，主刑伤阻滞",'points': points})

            if relationship_settings.get('地支相害', True) and zhi_atts[zhi1]['害'] == zhi2:
                points = 18 if (i >= 4 or j >= 4) and num_pillars == 6 else 12
                relationships.append({'type': '地支相害','positions': [i, j],'characters': [zhi1, zhi2],'description': "地支相害，主暗中损害",'points': points})

            if relationship_settings.get('地支相破', True) and zhi_atts[zhi1]['破'] == zhi2:
                points = 15 if (i >= 4 or j >= 4) and num_pillars == 6 else 10
                relationships.append({'type': '地支相破','positions': [i, j],'characters': [zhi1, zhi2],'description': "地支相破，主破坏损失",'points': points})

    # Check 三合 (triple harmonies)
    if relationship_settings.get('地支三合局', True):
        sanhe_patterns = [
            (['申', '子', '辰'], '申子辰三合水局'), (['寅', '午', '戌'], '寅午戌三合火局'),
            (['巳', '酉', '丑'], '巳酉丑三合金局'), (['亥', '卯', '未'], '亥卯未三合木局')
        ]
        for pattern, desc in sanhe_patterns:
            # This complex logic handles full combinations, partial combinations, and avoids duplicates
            # It's copied verbatim from the original BaziGame class
            positions, chars = [], []
            temp_zhis = list(zhis[:num_pillars])
            
            for p_char in pattern:
                if p_char in temp_zhis:
                    idx = temp_zhis.index(p_char)
                    positions.append(idx)
                    chars.append(p_char)
                    temp_zhis[idx] = None # Avoid reusing the same character
            
            if len(positions) == 3:
                points = 30 if any(p >= 4 for p in positions) and num_pillars == 6 else 20
                relationships.append({'type': '地支三合', 'positions': sorted(positions), 'characters': chars, 'description': desc, 'points': points})
            elif len(positions) == 2:
                points = 18 if any(p >= 4 for p in positions) and num_pillars == 6 else 12
                element_map = {'水':"水", '火':"火", '金':"金", '木':"木"}
                element = element_map.get(desc[-2])
                pair_tuple = tuple(sorted(chars))
                half_info = zhi_half_3hes.get(pair_tuple, zhi_half_3hes.get(tuple(reversed(pair_tuple)), ""))
                half_desc = f"{''.join(chars)}半合 {half_info}" if half_info else f"{''.join(chars)}半合化{element}"
                relationships.append({'type': '地支半合', 'positions': sorted(positions), 'characters': chars, 'description': half_desc, 'points': points})

    # Check 三会 (triple meetings)
    if relationship_settings.get('地支三会方', True):
        sanhui_patterns = [
            (['亥', '子', '丑'], '亥子丑三会水方'), (['寅', '卯', '辰'], '寅卯辰三会木方'),
            (['巳', '午', '未'], '巳午未三会火方'), (['申', '酉', '戌'], '申酉戌三会金方')
        ]
        for pattern, desc in sanhui_patterns:
            positions, chars = [], []
            temp_zhis = list(zhis[:num_pillars])
            for p_char in pattern:
                if p_char in temp_zhis:
                    idx = temp_zhis.index(p_char)
                    positions.append(idx)
                    chars.append(p_char)
                    temp_zhis[idx] = None # Avoid reusing
            
            if len(positions) == 3:
                points = 27 if any(p >= 4 for p in positions) and num_pillars == 6 else 18
                relationships.append({'type': '地支三会', 'positions': sorted(positions), 'characters': chars, 'description': desc, 'points': points})
            elif len(positions) == 2:
                points = 15 if any(p >= 4 for p in positions) and num_pillars == 6 else 10
                element_map = {'水':"水", '木':"木", '火':"火", '金':"金"}
                element = element_map.get(desc[-2])
                half_desc = f"{''.join(chars)}半会化{element}"
                relationships.append({'type': '地支半会', 'positions': sorted(positions), 'characters': chars, 'description': half_desc, 'points': points})

    return relationships