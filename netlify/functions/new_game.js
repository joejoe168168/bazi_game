exports.handler = async (event, context) => {
  // Handle CORS preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: ''
    };
  }

  try {
    // Parse request body
    const params = JSON.parse(event.body || '{}');
    const advancedMode = params.advanced_mode || false;
    const customSettings = params.settings || {};
    const birthDate = params.birth_date; // Optional birth date input
    
    // Default settings
    const defaultSettings = {
      '天干五合': true, '天干相冲': true,
      '地支相冲': true, '地支六合': true,
      '地支相刑': false, '地支三合局': true,
      '地支三会方': true, '地支暗合': true,
      '地支相害': false, '地支相破': false
    };
    
    // Merge settings
    const settings = { ...defaultSettings, ...customSettings };
    
    // Complete Bazi data structures
    const gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
    const zhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
    
    // Relationship data
    const ganHes = {
      '甲己': '中正之合 化土', '乙庚': '仁义之合 化金', '丙辛': '威制之合 化水',
      '丁壬': '淫慝之合 化木', '戊癸': '无情之合 化火'
    };
    
    const ganChongs = {
      '甲庚': '相冲', '乙辛': '相冲', '丙壬': '相冲', '丁癸': '相冲'
    };
    
    const zhi6hes = {
      '子丑': '土', '寅亥': '木', '卯戌': '火', '辰酉': '金', '巳申': '水', '午未': '土'
    };
    
    const zhiAtts = {
      "子": {"冲": "午", "刑": "卯", "六": "丑", "害": "未", "破": "酉"},
      "丑": {"冲": "未", "刑": "戌", "六": "子", "害": "午", "破": "辰"},
      "寅": {"冲": "申", "刑": "巳", "六": "亥", "害": "巳", "破": "亥"},
      "卯": {"冲": "酉", "刑": "子", "六": "戌", "害": "辰", "破": "午"},
      "辰": {"冲": "戌", "刑": "辰", "六": "酉", "害": "卯", "破": "丑"},
      "巳": {"冲": "亥", "刑": "申", "六": "申", "害": "寅", "破": "申"},
      "午": {"冲": "子", "刑": "午", "六": "未", "害": "丑", "破": "卯"},
      "未": {"冲": "丑", "刑": "丑", "六": "午", "害": "子", "破": "戌"},
      "申": {"冲": "寅", "刑": "寅", "六": "巳", "害": "亥", "破": "巳"},
      "酉": {"冲": "卯", "刑": "酉", "六": "辰", "害": "戌", "破": "子"},
      "戌": {"冲": "辰", "刑": "未", "六": "卯", "害": "酉", "破": "未"},
      "亥": {"冲": "巳", "刑": "亥", "六": "寅", "害": "申", "破": "寅"}
    };
    
    // Import Bazi calculator
    const BaziCalculator = require('./bazi_calculator');
    const calculator = new BaziCalculator();
    
    // Generate chart based on input type
    let chart;
    if (birthDate && birthDate.year && birthDate.month && birthDate.day) {
      // Generate from birth date
      const hour = birthDate.hour || 0;
      const isFemale = birthDate.is_female || false;
      chart = calculator.generateFromBirthDate(
        birthDate.year, 
        birthDate.month, 
        birthDate.day, 
        hour, 
        isFemale, 
        advancedMode
      );
    } else {
      // Generate random chart
      chart = calculator.generateRandom(advancedMode);
    }
    
    // Complete relationship detection
    const allRelationships = [];
    const numPillars = advancedMode ? 6 : 4;
    const chartGans = chart.gans;
    const chartZhis = chart.zhis;
    
    // 天干关系
    for (let i = 0; i < numPillars; i++) {
      for (let j = i + 1; j < numPillars; j++) {
        const gan1 = chartGans[i], gan2 = chartGans[j];
        const pair1 = gan1 + gan2;
        const pair2 = gan2 + gan1;
        const points = (i >= 4 || j >= 4) && numPillars === 6 ? 15 : 10;
        
        // 天干五合
        if (settings['天干五合'] && (ganHes[pair1] || ganHes[pair2])) {
          const relInfo = ganHes[pair1] || ganHes[pair2];
          const element = relInfo.match(/化([土金水木火])/)?.[1] || '';
          const desc = element ? `${gan1}${gan2}合化${element}` : `${gan1}${gan2}相合`;
          allRelationships.push({
            type: '天干五合', positions: [i, j], characters: [gan1, gan2],
            description: desc, full_description: relInfo, points: points + 5
          });
        }
        
        // 天干相冲
        if (settings['天干相冲'] && (ganChongs[pair1] || ganChongs[pair2])) {
          allRelationships.push({
            type: '天干相冲', positions: [i, j], characters: [gan1, gan2],
            description: '天干相冲，主冲突不和', points: points - 2
          });
        }
      }
    }
    
    // 地支关系
    for (let i = 0; i < numPillars; i++) {
      for (let j = i + 1; j < numPillars; j++) {
        const zhi1 = chartZhis[i], zhi2 = chartZhis[j];
        const points = (i >= 4 || j >= 4) && numPillars === 6 ? 18 : 12;
        const zhiPos1 = i + numPillars, zhiPos2 = j + numPillars;
        
        // 地支六合
        if (settings['地支六合'] && zhiAtts[zhi1]['六'] === zhi2) {
          const pair1 = zhi1 + zhi2;
          const pair2 = zhi2 + zhi1;
          const element = zhi6hes[pair1] || zhi6hes[pair2] || '';
          const desc = element ? `${zhi1}${zhi2}六合化${element}` : `${zhi1}${zhi2}六合`;
          allRelationships.push({
            type: '地支六合', positions: [zhiPos1, zhiPos2], characters: [zhi1, zhi2],
            description: desc, points: points
          });
        }
        
        // 地支相冲
        if (settings['地支相冲'] && zhiAtts[zhi1]['冲'] === zhi2) {
          allRelationships.push({
            type: '地支相冲', positions: [zhiPos1, zhiPos2], characters: [zhi1, zhi2],
            description: '地支相冲，主动荡变化', points: points - 2
          });
        }
        
        // 地支相刑
        if (settings['地支相刑'] && zhiAtts[zhi1]['刑'] === zhi2) {
          allRelationships.push({
            type: '地支相刑', positions: [zhiPos1, zhiPos2], characters: [zhi1, zhi2],
            description: '地支相刑，主刑伤阻滞', points: points + 3
          });
        }
        
        // 地支相害
        if (settings['地支相害'] && zhiAtts[zhi1]['害'] === zhi2) {
          allRelationships.push({
            type: '地支相害', positions: [zhiPos1, zhiPos2], characters: [zhi1, zhi2],
            description: '地支相害，主暗中损害', points: points
          });
        }
        
        // 地支相破
        if (settings['地支相破'] && zhiAtts[zhi1]['破'] === zhi2) {
          allRelationships.push({
            type: '地支相破', positions: [zhiPos1, zhiPos2], characters: [zhi1, zhi2],
            description: '地支相破，主破坏损失', points: points - 2
          });
        }
      }
    }
    
    // 地支三合局
    if (settings['地支三合局']) {
      const sanhePatterns = [
        {chars: ['申', '子', '辰'], desc: '申子辰三合水局'},
        {chars: ['寅', '午', '戌'], desc: '寅午戌三合火局'},
        {chars: ['巳', '酉', '丑'], desc: '巳酉丑三合金局'},
        {chars: ['亥', '卯', '未'], desc: '亥卯未三合木局'}
      ];
      
      for (const pattern of sanhePatterns) {
        const positions = [], chars = [];
        const tempZhis = [...chartZhis.slice(0, numPillars)];
        
        for (const pChar of pattern.chars) {
          const idx = tempZhis.indexOf(pChar);
          if (idx !== -1) {
            positions.push(idx);
            chars.push(pChar);
            tempZhis[idx] = null; // Avoid reusing
          }
        }
        
        if (positions.length === 3) {
          const points = positions.some(p => p >= 4) && numPillars === 6 ? 30 : 20;
          allRelationships.push({
            type: '地支三合', positions: positions.map(p => p + numPillars), characters: chars,
            description: pattern.desc, points: points
          });
        } else if (positions.length === 2) {
          const points = positions.some(p => p >= 4) && numPillars === 6 ? 18 : 12;
          const element = pattern.desc.slice(-2, -1);
          const desc = `${chars.join('')}半合化${element}`;
          allRelationships.push({
            type: '地支半合', positions: positions.map(p => p + numPillars), characters: chars,
            description: desc, points: points
          });
        }
      }
    }
    
    // 地支三会方
    if (settings['地支三会方']) {
      const sanhuiPatterns = [
        {chars: ['亥', '子', '丑'], desc: '亥子丑三会水方'},
        {chars: ['寅', '卯', '辰'], desc: '寅卯辰三会木方'},
        {chars: ['巳', '午', '未'], desc: '巳午未三会火方'},
        {chars: ['申', '酉', '戌'], desc: '申酉戌三会金方'}
      ];
      
      for (const pattern of sanhuiPatterns) {
        const positions = [], chars = [];
        const tempZhis = [...chartZhis.slice(0, numPillars)];
        
        for (const pChar of pattern.chars) {
          const idx = tempZhis.indexOf(pChar);
          if (idx !== -1) {
            positions.push(idx);
            chars.push(pChar);
            tempZhis[idx] = null; // Avoid reusing
          }
        }
        
        if (positions.length === 3) {
          const points = positions.some(p => p >= 4) && numPillars === 6 ? 27 : 18;
          allRelationships.push({
            type: '地支三会', positions: positions.map(p => p + numPillars), characters: chars,
            description: pattern.desc, points: points
          });
        } else if (positions.length === 2) {
          const points = positions.some(p => p >= 4) && numPillars === 6 ? 15 : 10;
          const element = pattern.desc.slice(-2, -1);
          const desc = `${chars.join('')}半会化${element}`;
          allRelationships.push({
            type: '地支半会', positions: positions.map(p => p + numPillars), characters: chars,
            description: desc, points: points
          });
        }
      }
    }
    
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
      body: JSON.stringify({
        chart: chart,
        all_relationships: allRelationships
      })
    };
    
  } catch (error) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
      body: JSON.stringify({ error: error.message })
    };
  }
};