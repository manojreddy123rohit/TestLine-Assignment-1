import json
import pandas as pd
import requests
from utils import (process_current_quiz_data, process_historical_quiz_data, create_expanded_options, analyze_and_recommend, calculate_topic_stats, prepare_visualization_data)

def main():
    # Step 1: Load data from APIs
    current_quiz_submission_url = "https://api.jsonserve.com/rJvd7g"
    current_quiz_endpoint_url = "https://www.jsonkeeper.com/b/LLQT"
    historical_quiz_url = "https://api.jsonserve.com/XgAgFJ"

    current_quiz_submission_data = requests.get(current_quiz_submission_url).json()
    current_quiz_endpoint_data = requests.get(current_quiz_endpoint_url).json()
    historical_quiz_data = requests.get(historical_quiz_url).json()

    # Step 2: Process Current Quiz Data
    current_quiz_df = process_current_quiz_data(current_quiz_endpoint_data)

    # Step 3: Process Historical Quiz Data
    historical_quiz_df = process_historical_quiz_data(historical_quiz_data)

    # Step 4: Clean accuracy and score data
    historical_quiz_df['accuracy'] = historical_quiz_df['accuracy'].str.rstrip(' %').astype(float) / 100
    historical_quiz_df['final_score'] = pd.to_numeric(historical_quiz_df['final_score'])

    # Step 5: Create expanded options
    current_quiz_expanded_df = create_expanded_options(current_quiz_df)

    # Step 6: Calculate rolling averages
    historical_quiz_df['rolling_accuracy'] = historical_quiz_df['accuracy'].rolling(window=3, min_periods=1).mean()
    historical_quiz_df['rolling_mistakes'] = historical_quiz_df['incorrect_answers'].rolling(window=3, min_periods=1).mean()
    historical_quiz_df['improvement_rate'] = historical_quiz_df['accuracy'].diff()

    # Step 7: Calculate topic statistics
    topic_stats = calculate_topic_stats(historical_quiz_df)

    # Step 8: Generate insights and recommendations
    insights, recommendations = analyze_and_recommend(historical_quiz_df, topic_stats)

    # Display results
    print("\n=== STUDENT PERFORMANCE ANALYSIS ===")
    print("\n1. PERFORMANCE OVERVIEW")
    print(f"• Overall Accuracy: {insights['trending']['overall_accuracy']:.1%}")
    print(f"• Recent Performance: {insights['trending']['recent_accuracy']:.1%}")
    print(f"• Trend: {'Improving' if insights['trending']['improvement'] else 'Needs Attention'}")
    print(f"• Average Mistakes Corrected: {insights['learning']['mistake_correction_rate']:.1f}")

    print("\n2. TOPIC MASTERY")
    print("\nStrong Topics (≥70% accuracy):")
    for topic in insights['topics']['strong']:
        print(f"• {topic}")
        
    print("\nWeak Topics (<60% accuracy):")
    for topic in insights['topics']['weak']:
        print(f"• {topic}")

    print("\n3. RECOMMENDED ACTIONS")
    print("\nPriority Actions:")
    for action in recommendations['priority_actions']:
        print(f"• {action}")

    print("\nStudy Strategy:")
    for strategy in recommendations['study_strategy']:
        print(f"• {strategy}")

    print("\nNext Steps:")
    for step in recommendations['next_steps']:
        print(f"• {step}")

    prepare_visualization_data(historical_quiz_df, insights, topic_stats)

if __name__ == "__main__":
    main()