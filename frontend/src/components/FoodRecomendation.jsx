import React, { useState } from 'react';
import axios from 'axios';
import './FoodReom.css';

const FoodRecommendation = () => {
  const [city, setCity] = useState('');
  const [preference, setPreference] = useState('any');
  const [cuisineType, setCuisineType] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Predefined cities for autocomplete
  const cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'];

  const handleRecommendation = async () => {
    setError('');
    if (!city) {
      setError('City is required.');
      return;
    }

    // Default to "any" if cuisineType is empty
    const finalCuisineType = cuisineType.trim() === '' ? 'any' : cuisineType;

    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:5000/prefrecommend', {
        params: {
          city,
          preference,
          cuisine_type: finalCuisineType,
        },
      });

      if (response.data && response.data.recommendations) {
        setRecommendations(response.data.recommendations);
      } else {
        setError('No recommendations found.');
        setRecommendations([]);
      }
    } catch (error) {
      setError('Error fetching recommendations.');
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
    
        <h1>Food Recommendation</h1>
        <div className="form-container">
  
  <div className="form-group">
    <input
      type="text"
      list="city-list"
      className="form-control input-enhanced"
      placeholder="Enter city"
      value={city}
      onChange={(e) => setCity(e.target.value)}
    />
    <datalist id="city-list">
      {cities.map((cityOption, index) => (
        <option key={index} value={cityOption} />
      ))}
    </datalist>

    <select
  className={`modern-select ${preference}`}
  value={preference}
  onChange={(e) => setPreference(e.target.value)}
>
  <option value="any">Any</option>
  <option value="veg">Vegetarian</option>
  <option value="non-veg">Non-Vegetarian</option>
</select>


    <input
      type="text"
      className="form-control input-enhanced"
      placeholder="Enter cuisine type"
      value={cuisineType}
      onChange={(e) => setCuisineType(e.target.value)}
    />

    <button className="btn enhanced-btn" onClick={handleRecommendation} disabled={loading}>
      {loading ? (
        <div className="loader"></div>
      ) : (
        'Get Recommendations'
      )}
    </button>
  </div>
</div>

      {error && <p className="error-text">{error}</p>}



{recommendations.length > 0 ? (
  <ul className="recommendation-list">
    {recommendations.map((food, index) => (
      <li key={index} className="recommendation-item">
        <div className="recommendation-content">
          <h3 className="food-name">{food.name}</h3>
          <p className="food-description">{food.description}</p>
          <div className="restaurant-section">
            <h4 className="restaurant-title">Recommended Restaurants:</h4>
            <ul className="restaurant-list">
              {food.restaurants.map((restaurant, restaurantIndex) => (
                <li key={restaurantIndex} className="restaurant-item">
                  {restaurant}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </li>
    ))}
  </ul>
) : (
  !loading && <p className="no-recommendations">No food recommendations to display.</p>
)}

    </div>
  );
};

export default FoodRecommendation;
