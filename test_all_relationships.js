// Comprehensive test for all relationship types
const newGameFunc = require('./netlify/functions/new_game.js');

async function testAllRelationshipTypes() {
  console.log('🧪 Testing All Relationship Types');
  console.log('=' .repeat(60));

  // Test multiple charts to ensure we hit different relationship types
  const testConfigs = [
    { name: '天干五合测试', settings: {'天干五合': true}, expectedTypes: ['天干五合'] },
    { name: '天干相冲测试', settings: {'天干相冲': true}, expectedTypes: ['天干相冲'] },
    { name: '地支六合测试', settings: {'地支六合': true}, expectedTypes: ['地支六合'] },
    { name: '地支相冲测试', settings: {'地支相冲': true}, expectedTypes: ['地支相冲'] },
    { name: '地支三合测试', settings: {'地支三合局': true}, expectedTypes: ['地支三合', '地支半合'] },
    { name: '地支三会测试', settings: {'地支三会方': true}, expectedTypes: ['地支三会', '地支半会'] },
    { name: '地支相刑测试', settings: {'地支相刑': true}, expectedTypes: ['地支相刑'] },
    { name: '全部关系测试', settings: {
      '天干五合': true, '天干相冲': true,
      '地支六合': true, '地支相冲': true, '地支相刑': true,
      '地支三合局': true, '地支三会方': true,
      '地支相害': true, '地支相破': true
    }, expectedTypes: ['天干五合', '天干相冲', '地支六合', '地支相冲', '地支相刑', '地支三合', '地支半合', '地支三会', '地支半会', '地支相害', '地支相破'] }
  ];

  const foundTypes = new Set();
  let totalTests = 0;
  let successfulTests = 0;

  for (const config of testConfigs) {
    console.log(`\n📋 ${config.name}:`);
    
    // Run multiple tests for each configuration to increase chances of finding relationships
    for (let attempt = 0; attempt < 5; attempt++) {
      totalTests++;
      
      const testEvent = {
        httpMethod: 'POST',
        body: JSON.stringify({
          advanced_mode: false,
          settings: config.settings
        })
      };

      try {
        const result = await newGameFunc.handler(testEvent, {});
        
        if (result.statusCode === 200) {
          const data = JSON.parse(result.body);
          const rels = data.all_relationships;
          
          if (rels.length > 0) {
            successfulTests++;
            const relTypes = [...new Set(rels.map(r => r.type))];
            relTypes.forEach(type => foundTypes.add(type));
            
            console.log(`  尝试 ${attempt + 1}: 找到 ${rels.length} 个关系: ${relTypes.join(', ')}`);
            
            // Show specific relationships for verification
            rels.forEach(rel => {
              console.log(`    - ${rel.type}: ${rel.characters.join('')} (${rel.description})`);
            });
            
            break; // Found some relationships, move to next config
          }
        }
      } catch (error) {
        console.error(`  ❌ 测试错误: ${error.message}`);
      }
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('📊 测试总结:');
  console.log(`总测试次数: ${totalTests}`);
  console.log(`成功测试次数: ${successfulTests}`);
  console.log(`发现的关系类型 (${foundTypes.size}):`, Array.from(foundTypes).sort());
  
  // Check if we found the key relationship types
  const keyTypes = ['天干五合', '地支六合', '地支相冲', '地支三合'];
  const missingTypes = keyTypes.filter(type => !foundTypes.has(type));
  
  if (missingTypes.length === 0) {
    console.log('✅ 所有关键关系类型都被测试到了！');
  } else {
    console.log('⚠️  未测试到的关键关系类型:', missingTypes);
  }

  console.log('\n🔍 特定测试 - 强制甲己组合:');
  await testSpecificCombinations();
}

async function testSpecificCombinations() {
  // Test with known combinations
  const testCombinations = [
    { gans: ['甲', '己', '丙', '丁'], expected: '甲己合化土' },
    { gans: ['乙', '庚', '丙', '丁'], expected: '乙庚合化金' },
    { gans: ['甲', '庚', '丙', '丁'], expected: '甲庚相冲' }
  ];

  for (const combo of testCombinations) {
    console.log(`测试组合: ${combo.gans.join('')} (期望: ${combo.expected})`);
    
    // Force specific random values to get our desired combination
    const originalRandom = Math.random;
    let callCount = 0;
    const ganIndices = combo.gans.map(gan => ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"].indexOf(gan));
    
    Math.random = () => {
      const value = ganIndices[callCount % ganIndices.length];
      callCount++;
      return value / 10; // Convert index to 0-1 range
    };

    const testEvent = {
      httpMethod: 'POST',
      body: JSON.stringify({
        advanced_mode: false,
        settings: { '天干五合': true, '天干相冲': true }
      })
    };

    try {
      const result = await newGameFunc.handler(testEvent, {});
      
      if (result.statusCode === 200) {
        const data = JSON.parse(result.body);
        const ganRels = data.all_relationships.filter(r => r.type.includes('天干'));
        
        if (ganRels.length > 0) {
          ganRels.forEach(rel => {
            console.log(`  ✅ 找到: ${rel.description}`);
          });
        } else {
          console.log(`  ❌ 未找到期望的关系`);
        }
      }
    } catch (error) {
      console.error(`  ❌ 错误: ${error.message}`);
    } finally {
      Math.random = originalRandom;
    }
  }
}

testAllRelationshipTypes();