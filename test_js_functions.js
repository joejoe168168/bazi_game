// Test JavaScript functions locally
const fs = require('fs');
const path = require('path');

// Load the new_game function
const newGamePath = path.join(__dirname, 'netlify', 'functions', 'new_game.js');
const newGameFunction = require(newGamePath);

// Test event
const testEvent = {
  httpMethod: 'POST',
  body: JSON.stringify({
    advanced_mode: false,
    settings: {
      '天干五合': true,
      '地支六合': true
    }
  })
};

const testContext = {};

// Test the function
console.log('Testing JavaScript new_game function...');
newGameFunction.handler(testEvent, testContext)
  .then(result => {
    console.log('Status:', result.statusCode);
    if (result.statusCode === 200) {
      const data = JSON.parse(result.body);
      console.log('✅ Function works!');
      console.log('Chart:', data.chart.year_gan + data.chart.year_zhi);
      console.log('Relationships found:', data.all_relationships.length);
    } else {
      console.log('❌ Function failed:', result.body);
    }
  })
  .catch(error => {
    console.error('❌ Error:', error.message);
  });