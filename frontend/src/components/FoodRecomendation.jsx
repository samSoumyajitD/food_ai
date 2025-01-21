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

      <div className="form-group">
        <input
          type="text"
          list="city-list"
          className="form-control"
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
          className="form-control"
          value={preference}
          onChange={(e) => setPreference(e.target.value)}
        >
          <option value="any">Any</option>
          <option value="veg">Vegetarian</option>
          <option value="non-veg">Non-Vegetarian</option>
        </select>

        <input
          type="text"
          className="form-control"
          placeholder="Enter cuisine type"
          value={cuisineType}
          onChange={(e) => setCuisineType(e.target.value)}
        />

        <button className="btn" onClick={handleRecommendation}>
          Get Recommendations
        </button>
      </div>

      {error && <p className="error-text">{error}</p>}

      {loading && <div className="loader"></div>}

      <ul className="recommendation-list">
        {recommendations.map((food, index) => (
          <li key={index} className="recommendation-item">
            <strong>{food.name}</strong>: {food.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FoodRecommendation;
