# Student Quiz Performance Analyzer

A comprehensive analysis tool for evaluating student quiz performance and providing personalized learning recommendations.

## Project Overview

This project analyzes student quiz performance data to:
- Track performance trends across different topics
- Identify strengths and weaknesses
- Generate personalized study recommendations
- Visualize performance metrics through an interactive dashboard

## Features

- **Performance Analysis**
  - Topic-wise performance tracking
  - Accuracy trends analysis
  - Mistake correction patterns
  - Learning effectiveness metrics

- **Personalized Recommendations**
  - Priority topics identification
  - Study strategy suggestions
  - Practice recommendations

- **Interactive Dashboard**
  - Performance timeline visualization
  - Topic performance comparison
  - Strength/weakness distribution
  - Text-based insights

## Setup Instructions

1. **Backend Setup**
```bash
# Clone the repository
git clone [repository-url]

# Install Python dependencies
pip install pandas numpy requests

# Navigate to backend directory
cd backend

# Run the analysis
python main.py
```

2. **Frontend Setup**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Install required packages
npm install recharts

# Start the development server
npm start
```

## Project Structure
```
quiz_analysis/
├── backend/
│   ├── main.py           # Main execution script
│   ├── utils.py          # Utility functions
│   └── output/           # Generated visualization data
│       └── viz_data.json
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── StudentDashboard.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
```

## Approach

1. **Data Processing**
   - Load quiz data from API endpoints
   - Clean and standardize data formats
   - Calculate performance metrics

2. **Analysis**
   - Generate performance insights
   - Identify learning patterns
   - Calculate topic-wise statistics

3. **Recommendation Generation**
   - Analyze weak areas
   - Generate personalized study strategies
   - Create actionable recommendations

4. **Visualization**
   - Interactive performance timeline
   - Topic performance comparison
   - Strength/weakness distribution
   - Comprehensive text insights

## API Endpoints
- Current Quiz Data: https://api.jsonserve.com/rJvd7g
- Quiz Endpoint Data: https://www.jsonkeeper.com/b/LLQT
- Historical Quiz Data: https://api.jsonserve.com/XgAgFJ

## Technologies Used
- Python (Data Analysis)
- React (Frontend)
- Recharts (Visualization)
- Pandas (Data Processing)

## Future Enhancements
1. Machine Learning integration for predictive analytics
2. Additional visualization types
3. Real-time data updates
4. Peer comparison features