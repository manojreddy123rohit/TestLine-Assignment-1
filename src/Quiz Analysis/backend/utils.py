import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

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

def prepare_visualization_data(historical_quiz_df, insights, topic_stats, recommendations, persona, performance_labels):
    viz_data = {
        'timelineData': [
            {
                'date': row['submitted_at'].strftime('%Y-%m-%d'),
                'accuracy': float(round(row['accuracy'] * 100, 2)),
                'mistakesCorrected': int(row['mistakes_corrected'])
            } for _, row in historical_quiz_df.iterrows()
        ],
        'topicPerformance': [
            {
                'name': str(topic),
                'accuracy': float(round(stats['avg_accuracy'] * 100, 2))
            } for topic, stats in topic_stats.iterrows()
        ],
        'insights': {
            'trending': {
                'recent_accuracy': float(insights['trending']['recent_accuracy']),
                'overall_accuracy': float(insights['trending']['overall_accuracy']),
                'improvement': bool(insights['trending']['improvement'])
            },
            'topics': {
                'strong': list(insights['topics']['strong']),
                'weak': list(insights['topics']['weak']),
                'needs_practice': list(insights['topics']['needs_practice'])
            },
            'learning': {
                'mistake_correction_rate': float(insights['learning']['mistake_correction_rate']),
                'recent_corrections': float(insights['learning']['recent_corrections'])
            }
        },
        'recommendations': {
            'priority_actions': list(recommendations['priority_actions']),
            'study_strategy': list(recommendations['study_strategy']),
            'next_steps': list(recommendations['next_steps'])
        },
        'persona': {
            'learning_type': str(persona['learning_type']),
            'key_traits': list(persona['key_traits']),
            'learning_style': list(persona['learning_style'])
        },
        'performance_labels': {
            'strengths': list(performance_labels['strengths']),
            'challenges': list(performance_labels['challenges'])
        }
    }
    
    os.makedirs('frontend/public/data', exist_ok=True)
    with open('frontend/public/data/viz_data.json', 'w') as f:
        json.dump(viz_data, f, default=str)
        
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

def generate_strength_labels(insights, topic_stats):
    strengths = []
    
    # Check topic mastery
    strong_topics = topic_stats[topic_stats['avg_accuracy'] >= 0.7]
    if not strong_topics.empty:
        top_topic = strong_topics.index[0]
        strengths.append(f"Master of {top_topic} ({strong_topics['avg_accuracy'].iloc[0]*100:.1f}% accuracy)")
    
    # Check improvement trend
    if insights['trending']['improvement']:
        strengths.append("Consistent Improver")
    
    # Check mistake correction pattern
    if insights['learning']['recent_corrections'] > insights['learning']['mistake_correction_rate']:
        strengths.append("Effective at Learning from Mistakes")
    
    # Check attempt consistency
    high_attempt_topics = topic_stats[topic_stats['attempt_count'] > 2].index.tolist()
    if high_attempt_topics:
        strengths.append(f"Dedicated Practice in {high_attempt_topics[0]}")
    
    return strengths

def generate_challenge_labels(insights, topic_stats):
    challenges = []
    
    # Check weak topics
    weak_topics = topic_stats[topic_stats['avg_accuracy'] < 0.6]
    if not weak_topics.empty:
        weakest_topic = weak_topics.index[0]
        challenges.append(f"Needs Focus on {weakest_topic} ({weak_topics['avg_accuracy'].iloc[0]*100:.1f}% accuracy)")
    
    # Check practice needs
    low_attempt_topics = topic_stats[topic_stats['attempt_count'] == 1].index.tolist()
    if low_attempt_topics:
        challenges.append(f"More Practice Needed in {low_attempt_topics[0]}")
    
    # Check mistake patterns
    if insights['learning']['recent_corrections'] < insights['learning']['mistake_correction_rate']:
        challenges.append("Room for Improvement in Mistake Correction")
    
    return challenges

def define_student_persona(insights, historical_quiz_df):
    # Calculate key metrics for persona definition
    performance_stability = historical_quiz_df['accuracy'].std()
    mistake_improvement = (insights['learning']['recent_corrections'] / 
                         insights['learning']['mistake_correction_rate'] 
                         if insights['learning']['mistake_correction_rate'] > 0 else 0)
    
    # Define persona characteristics
    persona = {
        'learning_type': '',
        'key_traits': [],
        'learning_style': []
    }
    
    # Determine Learning Type
    if insights['trending']['improvement'] and mistake_improvement > 1:
        persona['learning_type'] = "Active Improver"
    elif insights['trending']['improvement'] and mistake_improvement <= 1:
        persona['learning_type'] = "Steady Performer"
    elif not insights['trending']['improvement'] and mistake_improvement > 1:
        persona['learning_type'] = "Recovery Learner"
    else:
        persona['learning_type'] = "Needs Support"
        
    # Identify Key Traits
    if len(insights['topics']['strong']) >= 2:
        persona['key_traits'].append("Topic Master")
    if performance_stability < 0.15:  # Low variation in performance
        persona['key_traits'].append("Consistent Performer")
    if mistake_improvement > 1.2:
        persona['key_traits'].append("Quick Learner from Mistakes")
        
    # Define Learning Style
    if historical_quiz_df['mistakes_corrected'].mean() > 5:
        persona['learning_style'].append("Reflective Learner")
    if insights['trending']['recent_accuracy'] > 0.8:
        persona['learning_style'].append("High Achiever")
    if performance_stability > 0.25:  # High variation
        persona['learning_style'].append("Experimental Learner")
        
    return persona

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

    # Add persona analysis
    persona = define_student_persona(insights, historical_quiz_df)
    
    # Add creative labels for strengths and weaknesses
    performance_labels = {
        'strengths': generate_strength_labels(insights, topic_stats),
        'challenges': generate_challenge_labels(insights, topic_stats)
    }
    
    return insights, recommendations, persona, performance_labels

def calculate_topic_stats(historical_quiz_df):
    topic_stats = historical_quiz_df.groupby('quiz_topic').agg({
        'accuracy': ['mean', 'count'],
        'mistakes_corrected': ['sum', 'mean'],
        'improvement_rate': 'mean'
    }).round(3)
    
    topic_stats.columns = ['avg_accuracy', 'attempt_count', 'total_mistakes_corrected', 
                          'avg_mistakes_corrected', 'avg_improvement']
    
    return topic_stats.sort_values('avg_accuracy', ascending=False)

def prepare_visualization_data(historical_quiz_df, insights, topic_stats, recommendations, persona, performance_labels):
    viz_data = {
        'timelineData': [
            {
                'date': row['submitted_at'].strftime('%Y-%m-%d'),
                'accuracy': float(round(row['accuracy'] * 100, 2)),
                'mistakesCorrected': int(row['mistakes_corrected'])
            } for _, row in historical_quiz_df.iterrows()
        ],
        'topicPerformance': [
            {
                'name': str(topic),
                'accuracy': float(round(stats['avg_accuracy'] * 100, 2))
            } for topic, stats in topic_stats.iterrows()
        ],
        'insights': {
            'trending': {
                'recent_accuracy': float(insights['trending']['recent_accuracy']),
                'overall_accuracy': float(insights['trending']['overall_accuracy']),
                'improvement': bool(insights['trending']['improvement'])
            },
            'topics': {
                'strong': list(insights['topics']['strong']),
                'weak': list(insights['topics']['weak']),
                'needs_practice': list(insights['topics']['needs_practice'])
            },
            'learning': {
                'mistake_correction_rate': float(insights['learning']['mistake_correction_rate']),
                'recent_corrections': float(insights['learning']['recent_corrections'])
            }
        },
        'recommendations': {
            'priority_actions': list(recommendations['priority_actions']),
            'study_strategy': list(recommendations['study_strategy']),
            'next_steps': list(recommendations['next_steps'])
        },
        'persona': {
            'learning_type': str(persona['learning_type']),
            'key_traits': list(persona['key_traits']),
            'learning_style': list(persona['learning_style'])
        },
        'performance_labels': {
            'strengths': list(performance_labels['strengths']),
            'challenges': list(performance_labels['challenges'])
        }
    }
    
    os.makedirs('frontend/public/data', exist_ok=True)
    with open('frontend/public/data/viz_data.json', 'w') as f:
        json.dump(viz_data, f, default=str)

def create_visualizations(historical_quiz_df, topic_stats, insights):
    os.makedirs('output/visualizations', exist_ok=True)
    
    # Set consistent theme and color palette
    sns.set_theme(style="whitegrid", palette="viridis")
    plt.rcParams['figure.figsize'] = [12, 6]
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.size'] = 10
    
    # Color definitions
    COLORS = {
        'strong': '#4CAF50',  # Green
        'weak': '#FF5722',    # Red
        'neutral': '#FFC107', # Yellow
        'accent': '#2196F3'   # Blue
    }
    
    # 1. Performance Timeline
    plt.figure()
    # Convert accuracy to percentage
    accuracy_data = historical_quiz_df['accuracy'] * 100
    
    # Create dual axis plot
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot accuracy
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Accuracy (%)', color=COLORS['strong'])
    line1 = ax1.plot(historical_quiz_df['submitted_at'], accuracy_data, 
                     color=COLORS['strong'], marker='o', label='Accuracy')
    ax1.tick_params(axis='y', labelcolor=COLORS['strong'])
    
    # Create second axis for mistakes
    ax2 = ax1.twinx()
    ax2.set_ylabel('Mistakes Corrected', color=COLORS['accent'])
    line2 = ax2.plot(historical_quiz_df['submitted_at'], 
                     historical_quiz_df['mistakes_corrected'],
                     color=COLORS['accent'], marker='s', label='Mistakes Corrected')
    ax2.tick_params(axis='y', labelcolor=COLORS['accent'])
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.title('Performance Timeline', pad=20, size=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/visualizations/performance_timeline.png')
    plt.close()

    # 2. Topic Performance
    plt.figure()
    topic_data = topic_stats.reset_index()
    # Remove duplicates by averaging
    topic_data = topic_data.groupby('quiz_topic').agg({
        'avg_accuracy': 'mean'
    }).reset_index()
    
    # Sort by accuracy
    topic_data = topic_data.sort_values('avg_accuracy', ascending=True)
    
    colors = [COLORS['strong'] if x >= 0.7 else COLORS['weak'] if x < 0.6 
              else COLORS['neutral'] for x in topic_data['avg_accuracy']]
    
    bars = plt.barh(topic_data['quiz_topic'], topic_data['avg_accuracy'] * 100, 
                    color=colors)
    
    # Add value labels on bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}%', 
                va='center', ha='left', fontweight='bold')
    
    plt.title('Topic Performance Analysis', pad=20, size=14)
    plt.xlabel('Accuracy (%)')
    plt.ylabel('Topics')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('output/visualizations/topic_performance.png')
    plt.close()

    # 3. Topic Distribution
    plt.figure()
    # Remove duplicates from counts
    strong_topics = len(set(insights['topics']['strong']))
    weak_topics = len(set(insights['topics']['weak']))
    needs_practice = len(set(insights['topics']['needs_practice']))
    
    labels = ['Strong Topics', 'Weak Topics', 'Needs Practice']
    sizes = [strong_topics, weak_topics, needs_practice]
    colors = [COLORS['strong'], COLORS['weak'], COLORS['neutral']]
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
            startangle=90, explode=(0.05, 0.05, 0.05))
    plt.title('Topic Distribution', pad=20, size=14)
    plt.axis('equal')
    plt.savefig('output/visualizations/topic_distribution.png')
    plt.close()

    # 4. Learning Progress Heatmap
    plt.figure(figsize=(10, 6))
    progress_data = pd.DataFrame({
        'Metric': ['Accuracy (%)', 'Mistakes Corrected', 'Time (minutes)'],
        'Initial': [
            historical_quiz_df['accuracy'].iloc[0] * 100,
            historical_quiz_df['mistakes_corrected'].iloc[0],
            pd.to_numeric(historical_quiz_df['duration'].iloc[0].split(':')[0])
        ],
        'Middle': [
            historical_quiz_df['accuracy'].iloc[len(historical_quiz_df)//2] * 100,
            historical_quiz_df['mistakes_corrected'].iloc[len(historical_quiz_df)//2],
            pd.to_numeric(historical_quiz_df['duration'].iloc[len(historical_quiz_df)//2].split(':')[0])
        ],
        'Recent': [
            historical_quiz_df['accuracy'].iloc[-1] * 100,
            historical_quiz_df['mistakes_corrected'].iloc[-1],
            pd.to_numeric(historical_quiz_df['duration'].iloc[-1].split(':')[0])
        ]
    })
    progress_data = progress_data.set_index('Metric')

    sns.heatmap(progress_data, annot=True, cmap='RdYlGn', center=None,
                fmt='.1f', cbar_kws={'label': 'Value'})
    plt.title('Learning Progress Analysis', pad=20, size=14)
    plt.tight_layout()
    plt.savefig('output/visualizations/learning_progress.png')
    plt.close()

    print("\nEnhanced visualizations have been saved to 'output/visualizations/' directory:")
    print("1. performance_timeline.png - Interactive timeline with dual axis")
    print("2. topic_performance.png - Horizontal bar chart with value labels")
    print("3. topic_distribution.png - Exploded pie chart with percentages")
    print("4. learning_progress.png - Enhanced heatmap with better color scaling")