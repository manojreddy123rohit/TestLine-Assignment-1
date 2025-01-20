# Quiz Performance Analysis System

A comprehensive analysis tool that examines student quiz performance and provides personalized recommendations for NEET preparation.

## Project Overview

The system analyzes quiz performance data to:
- Track performance trends across different topics
- Identify strengths and weaknesses
- Generate personalized study recommendations
- Visualize performance metrics through interactive graphs

## Key Features

### 1. Performance Analysis
- Topic-wise performance tracking
- Accuracy trends over time
- Mistake correction patterns
- Learning effectiveness metrics

### 2. Personalized Recommendations
- Priority topics identification
- Custom study strategies
- Practice suggestions based on performance

### 3. Data Visualization
- Interactive performance timeline
- Topic performance comparison
- Strength/weakness distribution
- Learning progress heatmap

## Visualizations

### Performance Timeline
![Performance Timeline](output/visualizations/performance_timeline.png)
- Shows accuracy trends and mistakes corrected over time
- Helps track improvement patterns

### Topic Performance
![Topic Performance](output/visualizations/topic_performance.png)
- Displays performance across different topics
- Color-coded for easy identification of strong/weak areas

### Topic Distribution
![Topic Distribution](output/visualizations/topic_distribution.png)
- Shows distribution of topic mastery
- Helps identify areas needing focus

### Learning Progress
![Learning Progress](output/visualizations/learning_progress.png)
- Heatmap showing progress in key metrics
- Tracks improvement across different parameters

## Project Structure
```
quiz_analysis/
├── backend/
│   ├── main.py           # Main execution script
│   ├── utils.py          # Utility functions
│   └── output/           # Generated visualizations
│       └── visualizations/
│           └── *.png
│
├── frontend/             # Optional React dashboard
│   └── src/
│       └── components/
│           └── StudentDashboard.jsx
│
└── requirements.txt      # Project dependencies
```

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd quiz-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the analysis:
```bash
python backend/main.py
```

## Technologies Used
- Python
- Pandas (Data Processing)
- Matplotlib/Seaborn (Visualization)
- React (Optional Frontend)
- Recharts (Interactive Charts)

## Implementation Details

### Data Processing
- Loads quiz data from API endpoints
- Cleans and standardizes data formats
- Calculates performance metrics

### Analysis Components
- Topic performance analysis
- Time-based trend analysis
- Student persona identification
- Recommendation generation

### Visualization Components
- Performance timeline charts
- Topic performance bars
- Distribution pie charts
- Progress heatmaps

## API Endpoints
- Current Quiz Data: https://api.jsonserve.com/rJvd7g
- Quiz Endpoint Data: https://www.jsonkeeper.com/b/LLQT
- Historical Quiz Data: https://api.jsonserve.com/XgAgFJ

## Future Enhancements
1. Machine Learning integration for predictive analytics
2. Real-time data updates
3. Peer comparison features
4. Mobile app integration

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request