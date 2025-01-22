import requests
import google.generativeai as genai
import json
from config import WEATHER_API_KEY, GENAI_API_KEY

# Configure the Generative AI API
genai.configure(api_key=GENAI_API_KEY)

def get_weather_data(city):
    """
    Fetches weather data for the given city.
    """
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        return None, "Could not fetch weather details. Please check the city name."

    weather_data = weather_response.json()
    weather_main = weather_data['weather'][0]['main']
    temperature = weather_data['main']['temp']
    return {"main": weather_main, "temp": temperature}, None

def recommend_food_for_weather(city, preference="any", cuisine_type="any"):
    """
    Recommends food based on the weather of the given city, user preference (veg/non-veg/any),
    and type of cuisine (e.g., Indian, Continental, Chinese, etc.).
    """
    
    # Fetch weather data
    weather, error = get_weather_data(city)
    if error:
        return {"error": error}

    # Use Generative AI to suggest food
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        prompt = (
            f"The weather in {city} is {weather['main']} with a temperature of {weather['temp']}°C. "
            f"Suggest 25 {preference} food items from {cuisine_type} cuisine suitable for this weather and the restaurants in {city} that serve that food items. "
            f"Return the output in JSON format with name and description and list of restaurants."
        )
        response = model.generate_content(prompt)

        # Extract JSON response from the AI response
        json_start = response.text.find("{")
        json_end = response.text.rfind("}")
        food_data = response.text[json_start:json_end + 1]
        food_data_parsed = json.loads(food_data)

        # Ensure consistent JSON structure with "FoodSuggestions"
        if isinstance(food_data_parsed, dict):
            key_to_replace = next(iter(food_data_parsed))
            food_suggestions = food_data_parsed.get(key_to_replace, [])
            return {
                "city": city,
                "weather": weather,
                "preference": preference,
                "cuisine_type": cuisine_type,
                "FoodSuggestions": food_suggestions
            }

        return {"error": "Unexpected response structure from AI."}
    except Exception as e:
        return {"error": f"Error generating food recommendations: {str(e)}"}