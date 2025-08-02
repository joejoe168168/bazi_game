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
    
    // Basic data
    const gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
    const zhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
    
    // Generate random chart
    const numPillars = advancedMode ? 6 : 4;
    const chartGans = Array.from({length: numPillars}, () => gans[Math.floor(Math.random() * gans.length)]);
    const chartZhis = Array.from({length: numPillars}, () => zhis[Math.floor(Math.random() * zhis.length)]);
    
    const chart = {
      year_gan: chartGans[0],
      year_zhi: chartZhis[0],
      month_gan: chartGans[1],
      month_zhi: chartZhis[1],
      day_gan: chartGans[2],
      day_zhi: chartZhis[2],
      hour_gan: chartGans[3],
      hour_zhi: chartZhis[3],
      gans: chartGans,
      zhis: chartZhis,
      date_info: `随机八字 ${chartGans[0]}${chartZhis[0]} ${chartGans[1]}${chartZhis[1]} ${chartGans[2]}${chartZhis[2]} ${chartGans[3]}${chartZhis[3]}`,
      advanced_mode: advancedMode
    };
    
    if (advancedMode) {
      chart.dayun_gan = chartGans[4];
      chart.dayun_zhi = chartZhis[4];
      chart.liunian_gan = chartGans[5];
      chart.liunian_zhi = chartZhis[5];
      chart.current_year = 2024;
    }
    
    // Simple relationship detection
    const allRelationships = [];
    
    // Basic 天干相合 detection
    if (settings['天干五合']) {
      const ganHes = {
        '甲己': '合土', '乙庚': '合金', '丙辛': '合水', 
        '丁壬': '合木', '戊癸': '合火'
      };
      
      for (let i = 0; i < chartGans.length; i++) {
        for (let j = i + 1; j < chartGans.length; j++) {
          const pair = [chartGans[i], chartGans[j]].sort().join('');
          if (ganHes[pair]) {
            allRelationships.push({
              type: '天干相合',
              positions: [i, j],
              characters: [chartGans[i], chartGans[j]],
              description: `${chartGans[i]}${chartGans[j]}${ganHes[pair]}`,
              points: 10
            });
          }
        }
      }
    }
    
    // Basic 地支六合 detection
    if (settings['地支六合']) {
      const zhiHes = {
        '子丑': '合土', '寅亥': '合木', '卯戌': '合火',
        '辰酉': '合金', '巳申': '合水', '午未': '合土'
      };
      
      for (let i = 0; i < chartZhis.length; i++) {
        for (let j = i + 1; j < chartZhis.length; j++) {
          const pair = [chartZhis[i], chartZhis[j]].sort().join('');
          if (zhiHes[pair]) {
            allRelationships.push({
              type: '地支六合',
              positions: [i + numPillars, j + numPillars],
              characters: [chartZhis[i], chartZhis[j]],
              description: `${chartZhis[i]}${chartZhis[j]}${zhiHes[pair]}`,
              points: 8
            });
          }
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