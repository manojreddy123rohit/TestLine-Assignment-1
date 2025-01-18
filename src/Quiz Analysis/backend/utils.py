import pandas as pd
import json

def process_current_quiz_data(current_quiz_endpoint_data):
    current_quiz_questions = []
    for question in current_quiz_endpoint_data["quiz"]["questions"]:
        current_quiz_questions.append({
            "question_id": question["id"],
            "topic": question["topic"],
            "description": question["description"],
            "options": {option["id"]: option["description"] for option in question["options"]},
            "correct_option": next(option["description"] for option in question["options"] if option["is_correct"])
        })
    return pd.DataFrame(current_quiz_questions)

def process_historical_quiz_data(historical_quiz_data):
    historical_quiz_results = []
    for result in historical_quiz_data:
        historical_quiz_results.append({
            "quiz_id": result["quiz_id"],
            "quiz_topic": result["quiz"]["topic"],
            "score": result["score"],
            "accuracy": result["accuracy"],
            "final_score": result["final_score"],
            "mistakes_corrected": result["mistakes_corrected"],
            "correct_answers": result["correct_answers"],
            "incorrect_answers": result["incorrect_answers"],
            "duration": result["duration"],
            "submitted_at": pd.to_datetime(result["submitted_at"]),
            "response_map": result["response_map"]
        })
    
    historical_quiz_df = pd.DataFrame(historical_quiz_results)
    historical_quiz_df = historical_quiz_df.sort_values('submitted_at')
    return historical_quiz_df

def create_expanded_options(current_quiz_df):
    option_rows = []
    for _, row in current_quiz_df.iterrows():
        question_id = row['question_id']
        topic = row['topic']
        options_dict = row['options']
        correct_answer = row['correct_option']
        
        for option_id, option_text in options_dict.items():
            option_rows.append({
                'question_id': question_id,
                'topic': topic,
                'option_id': option_id,
                'option_text': option_text,
                'is_correct': option_text == correct_answer
            })
    
    return pd.DataFrame(option_rows)

def analyze_and_recommend(historical_quiz_df, topic_stats):
    # Generate Core Insights
    insights = {
        'trending': {
            'recent_accuracy': historical_quiz_df.tail(3)['accuracy'].mean(),
            'overall_accuracy': historical_quiz_df['accuracy'].mean(),
            'improvement': historical_quiz_df.tail(3)['accuracy'].mean() > historical_quiz_df['accuracy'].mean()
        },
        'topics': {
            'strong': topic_stats[topic_stats['avg_accuracy'] >= 0.7].index.tolist(),
            'weak': topic_stats[topic_stats['avg_accuracy'] < 0.6].index.tolist(),
            'needs_practice': topic_stats[topic_stats['attempt_count'] == 1].index.tolist()
        },
        'learning': {
            'mistake_correction_rate': historical_quiz_df['mistakes_corrected'].mean(),
            'recent_corrections': historical_quiz_df.tail(3)['mistakes_corrected'].mean()
        }
    }

    # Generate Recommendations
    recommendations = {
        'priority_actions': [],
        'study_strategy': [],
        'next_steps': []
    }

    for topic in insights['topics']['weak']:
        recommendations['priority_actions'].append(f"Prioritize {topic} - Performance below 60%")

    if insights['trending']['improvement']:
        recommendations['study_strategy'].append(
            f"Maintain current approach - Accuracy improved from {insights['trending']['overall_accuracy']:.1%} to {insights['trending']['recent_accuracy']:.1%}")
    else:
        recommendations['study_strategy'].append(
            f"Revise study approach - Recent accuracy ({insights['trending']['recent_accuracy']:.1%}) below overall ({insights['trending']['overall_accuracy']:.1%})")

    for topic in insights['topics']['needs_practice']:
        recommendations['next_steps'].append(f"Take more quizzes in {topic} to build mastery")

    return insights, recommendations

def calculate_topic_stats(historical_quiz_df):
    topic_stats = historical_quiz_df.groupby('quiz_topic').agg({
        'accuracy': ['mean', 'count'],
        'mistakes_corrected': ['sum', 'mean'],
        'improvement_rate': 'mean'
    }).round(3)
    
    topic_stats.columns = ['avg_accuracy', 'attempt_count', 'total_mistakes_corrected', 
                          'avg_mistakes_corrected', 'avg_improvement']
    
    return topic_stats.sort_values('avg_accuracy', ascending=False)

def prepare_visualization_data(historical_quiz_df, insights, topic_stats):
    # Convert Timestamp to string for submitted_at column
    historical_quiz_df['submitted_at'] = historical_quiz_df['submitted_at'].astype(str)
    
    # Convert topic_stats to a list of dictionaries, ensuring string keys
    topic_performance = topic_stats.reset_index().to_dict('records')
    
    # Create a JSON-serializable version of insights
    def make_json_serializable(obj):
        if isinstance(obj, dict):
            return {str(k): make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_json_serializable(item) for item in obj]
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)
    
    serializable_insights = make_json_serializable(insights)
    
    viz_data = {
        'timelineData': historical_quiz_df[['submitted_at', 'accuracy', 'mistakes_corrected']].to_dict('records'),
        'topicPerformance': topic_performance,
        'insights': serializable_insights
    }
    with open('output/viz_data.json', 'w') as f:
        json.dump(viz_data, f, indent=2) 