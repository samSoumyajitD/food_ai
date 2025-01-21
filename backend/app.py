from flask import Flask, request, jsonify
from ai_recommendations import prefered_ai_food_recommendation
from recommendations import recommend_food_for_weather
from fuzzywuzzy import process
import json
from flask_cors import CORS  # Import CORS
from config import CORS_ORIGIN

app = Flask(__name__)

# Enable CORS for localhost:3000
CORS(app, origins=CORS_ORIGIN)


# Load allowed cuisines from JSON file
with open('cuisines.json') as f:
    data = json.load(f)
ALLOWED_CUISINES = data["ALLOWED_CUISINES"]

# Allowed values for validation
VALID_PREFERENCES = ['veg', 'non-veg', 'any']

def fuzzy_match(input_value, valid_values):
    """
    Performs fuzzy matching to find the closest valid value for the input.
    Returns the best match if confidence is above a threshold, otherwise returns None.
    """
    match, score = process.extractOne(input_value, valid_values)
    return match if score > 80 else None

@app.route('/recommend', methods=['GET'])
def recommend():
    """
    API endpoint to get food recommendations based on city, preference (veg, non-veg, any),
    and cuisine type (e.g., Indian, Continental, etc.).
    """
    city = request.args.get('city')
    preference = request.args.get('preference', 'any').lower()
    cuisine_type = request.args.get('cuisine_type', 'any').lower()

    # Validate required parameters
    if not city:
        return jsonify({"error": "City is required."}), 400

    # Validate and correct preference parameter using fuzzy matching
    preference = fuzzy_match(preference, VALID_PREFERENCES)
    if not preference:
        return jsonify({
            "error": f"Invalid preference. Choose from {', '.join(VALID_PREFERENCES)}."
        }), 400

    # Validate and correct cuisine type parameter using fuzzy matching
    cuisine_type = fuzzy_match(cuisine_type, ALLOWED_CUISINES)
    if not cuisine_type:
        return jsonify({
            "error": f"Invalid cuisine type. Choose from {', '.join(ALLOWED_CUISINES)}."
        }), 400

    # Get recommendations
    recommendations = recommend_food_for_weather(city, preference, cuisine_type)
    if "error" in recommendations:
        return jsonify({"error": recommendations["error"]}), 500

    # Construct and return response
    return jsonify({
        "city": city,
        "preference": preference,
        "cuisine_type": cuisine_type,
        "weather": recommendations.get("weather", {}),
        "recommendations": recommendations.get("FoodSuggestions", [])
    })

@app.route('/prefrecommend', methods=['GET'])
def prefered_food_recommend():
    """
    API endpoint to get AI-filtered food recommendations based on user preferences.
    """
    try:
        # Extract query parameters
        city = request.args.get('city')
        preference = request.args.get('preference', 'any').lower()
        cuisine_type = request.args.get('cuisine_type', 'any').lower()
        
        # Validate query parameters
        if not city:
            return jsonify({"error": "Missing required parameter: city"}), 400

        # Validate and correct preference parameter using fuzzy matching
        preference = fuzzy_match(preference, VALID_PREFERENCES)
        if not preference:
            return jsonify({
                "error": f"Invalid preference. Choose from {', '.join(VALID_PREFERENCES)}."
            }), 400

        # Validate and correct cuisine type parameter using fuzzy matching
        cuisine_type = fuzzy_match(cuisine_type, ALLOWED_CUISINES)
        if not cuisine_type:
            return jsonify({
                "error": f"Invalid cuisine type. Choose from {', '.join(ALLOWED_CUISINES)}."
            }), 400
        
        # Get food recommendations
        recommendations = prefered_ai_food_recommendation(city, preference, cuisine_type)
        
        # Check for errors in recommendations
        if isinstance(recommendations, dict) and "error" in recommendations:
            return jsonify({"status": "error", "message": recommendations["error"]}), 400

        # Return the recommendations as JSON
        return jsonify({"status": "success", "recommendations": recommendations}), 200

    except Exception as e:
        # Return error details for debugging
        return jsonify({"status": "error", "message": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
