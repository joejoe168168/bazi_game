// Debug test for 甲己 relationship detection
const newGameFunc = require('./netlify/functions/new_game.js');

async function testJiaJiDetection() {
  console.log('🔍 Testing 甲己 Relationship Detection');
  console.log('=' .repeat(50));

  // Test with a forced chart that has 甲己
  console.log('\n1. Testing with forced 甲己 chart...');
  
  // Let's check the gan detection logic directly
  const gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
  const testGans = ["甲", "己", "丙", "丁"]; // Force 甲己 in positions 0,1
  
  console.log('Test gans:', testGans);
  
  // Check the pair detection logic
  const ganHes = {
    '甲己': '中正之合 化土', '乙庚': '仁义之合 化金', '丙辛': '威制之合 化水',
    '丁壬': '淫慝之合 化木', '戊癸': '无情之合 化火'
  };
  
  console.log('\n2. Testing pair detection logic...');
  for (let i = 0; i < testGans.length; i++) {
    for (let j = i + 1; j < testGans.length; j++) {
      const gan1 = testGans[i], gan2 = testGans[j];
      const pair = [gan1, gan2].sort().join('');
      console.log(`Checking positions [${i},${j}]: ${gan1}${gan2} -> sorted pair: "${pair}"`);
      
      if (ganHes[pair]) {
        console.log(`✅ Found relationship: ${ganHes[pair]}`);
      } else {
        console.log(`❌ No relationship found for pair "${pair}"`);
      }
    }
  }
  
  // Test with actual function call
  console.log('\n3. Testing with actual function call...');
  
  // Temporarily modify the function to use our test data
  const originalRandom = Math.random;
  let callCount = 0;
  Math.random = () => {
    // Force specific gans: 甲(0), 己(5), 丙(2), 丁(3)
    const values = [0, 5, 2, 3, 0, 5, 2, 3]; // Repeat for zhis too
    return values[callCount++ % values.length] / 10;
  };
  
  const testEvent = {
    httpMethod: 'POST',
    body: JSON.stringify({
      advanced_mode: false,
      settings: { '天干五合': true }
    })
  };

  try {
    const result = await newGameFunc.handler(testEvent, {});
    
    if (result.statusCode === 200) {
      const data = JSON.parse(result.body);
      const chart = data.chart;
      const rels = data.all_relationships;
      
      console.log('Generated chart gans:', chart.gans);
      console.log('Generated relationships:', rels.length);
      
      const ganRels = rels.filter(r => r.type === '天干五合');
      console.log('天干五合 relationships:', ganRels);
      
      if (ganRels.length > 0) {
        console.log('✅ Found 天干五合 relationships!');
        ganRels.forEach(rel => {
          console.log(`  - ${rel.characters.join('')}: ${rel.description}`);
        });
      } else {
        console.log('❌ No 天干五合 relationships found!');
      }
    } else {
      console.log('❌ Function call failed:', result.body);
    }
  } catch (error) {
    console.error('❌ Test error:', error.message);
  } finally {
    // Restore original Math.random
    Math.random = originalRandom;
  }

  console.log('\n' + '='.repeat(50));
}

testJiaJiDetection();