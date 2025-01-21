# AI Food Weather Based Recommendation System

This project is a web-based application that provides food recommendations based on weather conditions, user preferences (vegetarian, non-vegetarian, or any), and cuisine type. The backend is built with Flask and integrates AI-based recommendation logic, while the frontend is developed using React.

---

## Features
1. **Weather-Based Food Recommendations**: Fetches weather data for a given city and suggests food items suited to the current weather.
2. **User Preferences**: Allows users to specify dietary preferences (vegetarian, non-vegetarian, or any) and cuisine type.
3. **AI-Enhanced Recommendations**: Filters and refines recommendations using trained models and AI-based logic.
4. **Responsive Frontend**: Provides a clean and interactive UI for users to input their preferences and view recommendations.

---

## Technologies Used
### Backend
- **Flask**: A lightweight Python web framework.
- **scikit-learn**: For AI-based filtering and recommendation logic.
- **Google Generative AI API**: To enhance food suggestions based on weather and user inputs.
- **OpenWeatherMap API**: For fetching real-time weather data.
- **Flask-CORS**: To handle cross-origin requests.
- **FuzzyWuzzy**: For fuzzy matching of inputs (e.g., city names, cuisine types).

### Frontend
- **React**: For building a responsive user interface.
- **Axios**: For making API calls to the Flask backend.
- **CSS**: Custom styles for a clean UI.

---

## Application Structure
```
project-root/
│
├── backend/
│   ├── ai_recommendations.py
│   ├── app.py
│   ├── config.py
│   ├── cuisines.json
│   ├── myFood.json
│   ├── recommendations.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── FoodRecommendation.jsx
│   │   │   └── FoodReom.css
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── index.css
│   │   └── index.js
│   └── package.json
│
└── README.md
```

---

## Prerequisites
1. **Python 3.8+**
2. **Node.js 14+**
3. **npm or Yarn**
4. API Keys for:
   - OpenWeatherMap API
   - Google Generative AI

---

## Installation Guide

### Backend Setup
1. **Navigate to the `backend` directory**:
   ```
   cd backend
   ```
2. **Install Python dependencies**:
   ```
   pip install -r requirements.txt
   ```
3. **Set up the `.env` file**:
   Create a `.env` file in the `backend` directory with the following keys:
   ```
   WEATHER_API_KEY=<Your_OpenWeatherMap_API_Key>
   GENAI_API_KEY=<Your_Generative_AI_API_Key>
   CORS_ORIGIN=http://localhost:3000
   ```
4. **Run the Flask application**:
   ```
   python app.py
   ```
   The backend will run on `http://127.0.0.1:5000`.

### Frontend Setup
1. **Navigate to the `frontend` directory**:
   ```
   cd frontend
   ```
2. **Install Node.js dependencies**:
   ```
   npm install
   ```
3. **Run the React application**:
   ```
   npm start
   ```
   The frontend will run on `http://localhost:3000`.

---

## Usage
1. Open the browser and navigate to `http://localhost:3000`.
2. Enter a city name and specify your preferences:
   - Dietary preference (vegetarian, non-vegetarian, or any).
   - Cuisine type (e.g., Indian, Continental, etc.).
3. Click on the "Get Recommendations" button.
4. View the list of recommended food items along with their descriptions.

---

## Dependencies
### Backend
- `flask`
- `flask-cors`
- `requests`
- `scikit-learn`
- `google-generativeai`
- `python-dotenv`
- `fuzzywuzzy`

Install all dependencies via:
```bash
pip install -r requirements.txt
```

### Frontend
- `react`
- `axios`

Install all dependencies via:
```bash
npm install
```

---

## Example Workflow
1. **Input**:
   - City: `New York`
   - Preference: `Veg`
   - Cuisine Type: `Indian`
2. **Backend Process**:
   - Fetch weather data for New York.
   - Use the weather and user inputs to request food suggestions from the Generative AI API.
   - Filter and refine results using the trained AI model.
3. **Output**:
   - A list of vegetarian Indian food items suitable for the current weather in New York.

---

## AI and NLP Techniques Employed

### 1. **TF-IDF Vectorization (Term Frequency-Inverse Document Frequency)**
To transform textual data (such as food names and descriptions) into numerical feature representations, we utilize **TF-IDF Vectorization** through the `TfidfVectorizer` from **scikit-learn**. This technique efficiently captures the importance of words within a given corpus by weighing them based on both their frequency within a document and their uniqueness across the entire dataset. By representing text in this way, the system is able to analyze and compare food descriptions in a structured, high-dimensional feature space, facilitating precise recommendation filtering.

### 2. **Cosine Similarity for Textual Matching**
To assess the similarity between the user-preferred food items and the available recommendations, we leverage **Cosine Similarity**. This metric measures the angular distance between two vectors in a multi-dimensional space, where smaller angles indicate higher similarity. By using this method to compare the TF-IDF vectors of food descriptions, we effectively identify the most relevant food items aligned with user preferences, enhancing recommendation accuracy.

### 3. **Fuzzy String Matching with FuzzyWuzzy**
To account for input inconsistencies, typographical errors, or vague user queries (such as city names or cuisine types), we incorporate **FuzzyWuzzy**, a Python library that enables **fuzzy string matching**. FuzzyWuzzy employs a **Levenshtein Distance** algorithm to measure the difference between sequences, allowing the system to intelligently identify the closest valid match from a list of predefined values. This approach ensures robustness in handling user input variations and improves the system's resilience to imperfect data.

--- 

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

---

