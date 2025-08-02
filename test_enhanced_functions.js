// Test the enhanced JavaScript functions
const newGameFunc = require('./netlify/functions/new_game.js');
const checkRelFunc = require('./netlify/functions/check_relationship.js');

async function testEnhancedFunctions() {
  console.log('🧪 Testing Enhanced JavaScript Functions');
  console.log('=' .repeat(50));

  // Test 1: Generate a new game
  console.log('\n1. Testing new_game function...');
  const newGameEvent = {
    httpMethod: 'POST',
    body: JSON.stringify({
      advanced_mode: false,
      settings: {
        '天干五合': true,
        '天干相冲': true,
        '地支六合': true,
        '地支相冲': true,
        '地支相刑': true,
        '地支三合局': true,
        '地支三会方': true
      }
    })
  };

  try {
    const newGameResult = await newGameFunc.handler(newGameEvent, {});
    
    if (newGameResult.statusCode === 200) {
      const gameData = JSON.parse(newGameResult.body);
      const chart = gameData.chart;
      const allRels = gameData.all_relationships;
      
      console.log('✅ New game created successfully!');
      console.log(`📊 Chart: ${chart.year_gan}${chart.year_zhi} ${chart.month_gan}${chart.month_zhi} ${chart.day_gan}${chart.day_zhi} ${chart.hour_gan}${chart.hour_zhi}`);
      console.log(`🔗 Total relationships: ${allRels.length}`);
      
      // Count relationship types
      const relTypes = {};
      allRels.forEach(rel => {
        relTypes[rel.type] = (relTypes[rel.type] || 0) + 1;
      });
      
      console.log('📋 Relationship breakdown:');
      Object.entries(relTypes).forEach(([type, count]) => {
        console.log(`   ${type}: ${count}`);
      });

      // Test 2: Check a relationship
      if (allRels.length > 0) {
        console.log('\n2. Testing check_relationship function...');
        const testRel = allRels[0];
        console.log(`🎯 Testing relationship: ${testRel.type} - ${testRel.characters.join('')}`);
        
        const checkEvent = {
          httpMethod: 'POST',
          body: JSON.stringify({
            positions: testRel.positions,
            chart: chart,
            all_relationships: allRels,
            found_relationships: []
          })
        };

        const checkResult = await checkRelFunc.handler(checkEvent, {});
        
        if (checkResult.statusCode === 200) {
          const checkData = JSON.parse(checkResult.body);
          if (checkData.found) {
            console.log('✅ Relationship check successful!');
            console.log(`📍 Found: ${checkData.relationship.type} - ${checkData.relationship.description}`);
          } else {
            console.log('❌ Relationship check failed:', checkData.message);
          }
        } else {
          console.log('❌ Check relationship API failed:', checkResult.body);
        }

        // Test 3: Test duplicate detection
        console.log('\n3. Testing duplicate detection...');
        const duplicateEvent = {
          httpMethod: 'POST',
          body: JSON.stringify({
            positions: testRel.positions,
            chart: chart,
            all_relationships: allRels,
            found_relationships: [testRel] // Already found
          })
        };

        const dupResult = await checkRelFunc.handler(duplicateEvent, {});
        if (dupResult.statusCode === 200) {
          const dupData = JSON.parse(dupResult.body);
          if (!dupData.found) {
            console.log('✅ Duplicate detection working!');
            console.log(`📝 Message: ${dupData.message}`);
          } else {
            console.log('❌ Duplicate detection failed - should not find already found relationship');
          }
        }
      }

    } else {
      console.log('❌ New game failed:', newGameResult.body);
    }

  } catch (error) {
    console.error('❌ Test error:', error.message);
  }

  console.log('\n' + '='.repeat(50));
  console.log('🎉 Enhanced function testing complete!');
}

testEnhancedFunctions();