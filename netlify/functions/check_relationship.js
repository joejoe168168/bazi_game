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
    // Get request data
    const data = JSON.parse(event.body || '{}');
    const positions = data.positions || [];
    const chart = data.chart;
    const allRelationships = data.all_relationships || [];
    const foundRelationships = data.found_relationships || [];
    
    // Basic validation
    if (!chart || !positions.length) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
        body: JSON.stringify({ error: 'Missing required data: chart and positions.' })
      };
    }
    
    if (positions.length < 2 || positions.length > 3) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
        body: JSON.stringify({ error: 'Invalid number of positions selected' })
      };
    }

    // Normalize positions for comparison
    const sortedPositions = positions.sort((a, b) => a - b);
    
    // Check if this exact combination of positions has already been found
    for (const rel of foundRelationships) {
      const foundPositions = rel.actual_positions || rel.positions || [];
      if (JSON.stringify(foundPositions.sort((a, b) => a - b)) === JSON.stringify(sortedPositions)) {
        return {
          statusCode: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
          },
          body: JSON.stringify({ found: false, message: 'This relationship has already been found.' })
        };
      }
    }

    // Find a matching relationship from the pre-calculated list
    let foundMatch = null;
    for (const rel of allRelationships) {
      // Check if positions match any relationship
      const relPositions = rel.positions.sort((a, b) => a - b);
      if (JSON.stringify(relPositions) === JSON.stringify(sortedPositions)) {
        // Check if this EXACT combination of positions has been found before
        let isAlreadyFound = false;
        for (const foundRel of foundRelationships) {
          const foundPositions = (foundRel.actual_positions || foundRel.positions || []).sort((a, b) => a - b);
          if (foundRel.type === rel.type && 
              JSON.stringify(foundPositions) === JSON.stringify(sortedPositions)) {
            isAlreadyFound = true;
            break;
          }
        }
        
        if (!isAlreadyFound) {
          foundMatch = rel;
          break;
        }
      }
    }

    if (foundMatch) {
      // Add the actual positions from user selection to the found relationship
      const responseRel = { ...foundMatch };
      responseRel.actual_positions = sortedPositions;

      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
        body: JSON.stringify({ found: true, relationship: responseRel })
      };
    } else {
      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
        body: JSON.stringify({ found: false, message: 'No valid relationship found for the selection.' })
      };
    }

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