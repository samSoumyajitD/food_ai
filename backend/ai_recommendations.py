import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommendations import recommend_food_for_weather

def train_food_preference_model(training_data):
    """
    Train a preference model using both the name and description of food items.
    Returns a vectorizer and feature matrix.
    """
    # Combine name and description for training
    training_texts = [f"{item['name']} {item['description']}" for item in training_data]
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(training_texts)
    return vectorizer, feature_matrix

def recommend_food_from_preferences(recommended_foods, vectorizer, feature_matrix):
    """
    Filter recommended foods based on the trained preference model.
    """
    # Combine name and description for the recommendations
    recommended_texts = [f"{food['name']} {food['description']}" for food in recommended_foods]
    query_matrix = vectorizer.transform(recommended_texts)
    similarity_scores = cosine_similarity(query_matrix, feature_matrix)
    
    # Sort by similarity scores
    sorted_indices = similarity_scores.max(axis=1).argsort()[::-1]  # Descending order
    
    # Return at least 10 and at most 20 foods
    num_to_return = min(max(10, len(recommended_foods)), 20)
    return [recommended_foods[i] for i in sorted_indices[:num_to_return]]

def prefered_ai_food_recommendation(city, preference="any", cuisine_type="any"):
    """
    Get AI-filtered food recommendations.
    """
    # Load training data
    with open('myFood.json', 'r') as f:
        training_data = json.load(f)
    
    # Train preference model
    vectorizer, feature_matrix = train_food_preference_model(training_data)
    
    # Get recommendations
    food_suggestions = recommend_food_for_weather(city, preference, cuisine_type).get('FoodSuggestions', [])
    
    # Filter based on preferences
    filtered_food = recommend_food_from_preferences(food_suggestions, vectorizer, feature_matrix)
    
    return filtered_food


