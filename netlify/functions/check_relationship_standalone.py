import json

def handler(event, context):
    """
    Standalone check relationship function
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
        # Get all necessary data from the frontend
        data = json.loads(event.get('body', '{}'))
        positions = data.get('positions', [])
        chart = data.get('chart')
        all_relationships = data.get('all_relationships', [])
        found_relationships = data.get('found_relationships', [])
        
        # Basic validation
        if not all([chart, positions]):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({'error': 'Missing required data: chart and positions.'})
            }
        
        if len(positions) < 2 or len(positions) > 3:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({'error': 'Invalid number of positions selected'})
            }

        # Normalize positions for comparison
        sorted_positions = sorted(positions)
        
        # Check if this exact combination of positions has already been found
        for rel in found_relationships:
            if sorted(rel.get('actual_positions', [])) == sorted_positions:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                    },
                    'body': json.dumps({'found': False, 'message': 'This relationship has already been found.'})
                }

        # Find a matching relationship from the pre-calculated list
        found_match = None
        for rel in all_relationships:
            # Check if positions match any relationship
            if sorted(rel['positions']) == sorted_positions:
                # Check if this EXACT combination of positions has been found before
                is_already_found = False
                for found_rel in found_relationships:
                    if (found_rel['type'] == rel['type'] and 
                        sorted(found_rel.get('actual_positions', found_rel['positions'])) == sorted_positions):
                        is_already_found = True
                        break
                
                if not is_already_found:
                    found_match = rel
                    break

        if found_match:
            # Add the actual positions from user selection to the found relationship
            response_rel = found_match.copy()
            response_rel['actual_positions'] = sorted_positions

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({'found': True, 'relationship': response_rel}, ensure_ascii=False)
            }
        else:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({'found': False, 'message': 'No valid relationship found for the selection.'}, ensure_ascii=False)
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