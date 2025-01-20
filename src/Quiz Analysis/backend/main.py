import json
import pandas as pd
import requests
from utils import (
    process_current_quiz_data, 
    process_historical_quiz_data, 
    create_expanded_options, 
    analyze_and_recommend, 
    calculate_topic_stats, 
    prepare_visualization_data,
    create_visualizations  # Add this new import
)

def main():
    # Step 1: Load data from APIs
    current_quiz_submission_url = "https://api.jsonserve.com/rJvd7g"
    current_quiz_endpoint_url = "https://www.jsonkeeper.com/b/LLQT"
    historical_quiz_url = "https://api.jsonserve.com/XgAgFJ"

    try:
        current_quiz_submission_data = requests.get(current_quiz_submission_url).json()
        current_quiz_endpoint_data = requests.get(current_quiz_endpoint_url).json()
        historical_quiz_data = requests.get(historical_quiz_url).json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

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
    insights, recommendations, persona, performance_labels = analyze_and_recommend(historical_quiz_df, topic_stats)

    # Step 9: Generate visualizations
    create_visualizations(historical_quiz_df, topic_stats, insights)

    # Display results
    print("\n" + "="*50)
    print("        STUDENT PERFORMANCE ANALYSIS REPORT        ")
    print("="*50)

    print("\n1. PERFORMANCE OVERVIEW")
    print("-"*30)
    print(f"• Overall Accuracy: {insights['trending']['overall_accuracy']:.1%}")
    print(f"• Recent Performance: {insights['trending']['recent_accuracy']:.1%}")
    print(f"• Trend: {'Improving' if insights['trending']['improvement'] else 'Needs Attention'}")
    print(f"• Average Mistakes Corrected: {insights['learning']['mistake_correction_rate']:.1f}")

    print("\n2. TOPIC MASTERY")
    print("-"*30)
    print("\nStrong Topics (≥70% accuracy):")
    for topic in insights['topics']['strong']:
        print(f"• {topic}")
    
    print("\nWeak Topics (<60% accuracy):")
    for topic in insights['topics']['weak']:
        print(f"• {topic}")

    print("\n3. RECOMMENDED ACTIONS")
    print("-"*30)
    print("\nPriority Actions:")
    for action in recommendations['priority_actions']:
        print(f"• {action}")

    print("\nStudy Strategy:")
    for strategy in recommendations['study_strategy']:
        print(f"• {strategy}")

    print("\nNext Steps:")
    for step in recommendations['next_steps']:
        print(f"• {step}")

    print("\n4. STUDENT PERSONA")
    print("-"*30)
    print(f"Learning Type: {persona['learning_type']}")
    
    print("\nKey Traits:")
    for trait in persona['key_traits']:
        print(f"• {trait}")
    
    print("\nLearning Style:")
    for style in persona['learning_style']:
        print(f"• {style}")

    print("\n5. PERFORMANCE LABELS")
    print("-"*30)
    print("\nStrengths:")
    for strength in performance_labels['strengths']:
        print(f"• {strength}")
    
    print("\nChallenges:")
    for challenge in performance_labels['challenges']:
        print(f"• {challenge}")

    # Save data for visualization
    prepare_visualization_data(historical_quiz_df, insights, topic_stats, recommendations, persona, performance_labels)
    
    print("\n" + "="*50)
    print("Analysis complete. Check 'output/visualizations' for detailed graphs.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()