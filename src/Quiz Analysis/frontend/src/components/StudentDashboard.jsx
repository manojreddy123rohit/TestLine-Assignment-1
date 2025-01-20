import React, { useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  BarChart, Bar, PieChart, Pie, Cell, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, Radar
} from 'recharts';

const sampleData = {
  timelineData: [
    { date: '2025-01-17', accuracy: 90, mistakesCorrected: 9 },
    { date: '2025-01-16', accuracy: 100, mistakesCorrected: 3 },
    { date: '2025-01-15', accuracy: 96, mistakesCorrected: 11 }
  ],
  topicPerformance: [
    { name: 'Human Physiology', accuracy: 72 },
    { name: 'Reproductive Health', accuracy: 43 },
    { name: 'Human Reproduction', accuracy: 38 }
  ],
  insights: {
    trending: {
      overall_accuracy: 0.72,
      recent_accuracy: 0.85,
      improvement: true
    },
    topics: {
      strong: ['Human Physiology'],
      weak: ['Reproductive Health', 'Human Reproduction'],
      needs_practice: ['Reproductive Health']
    },
    learning: {
      mistake_correction_rate: 2.8,
      recent_corrections: 3.2
    }
  },
  performance_labels: {
    strengths: ["Master of Human Physiology (72% accuracy)", "Consistent Improver"],
    challenges: ["Needs Focus on Reproductive Health (43% accuracy)"]
  },
  recommendations: {
    priority_actions: ["Prioritize Reproductive Health - Performance below 60%"]
  },
  persona: {
    key_traits: ["Topic Master", "Quick Learner from Mistakes"],
    learning_style: ["High Achiever", "Reflective Learner"]
  }
};

const StudentDashboard = () => {
  const [dashboardData] = useState(sampleData);
  const COLORS = ['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0'];

  const MetricCard = ({ title, children, className = '' }) => (
    <div className={`bg-green-50 rounded-lg shadow-sm p-6 ${className}`}>
      <h3 className="text-xl font-semibold text-gray-800 mb-4">{title}</h3>
      {children}
    </div>
  );

  const ListCard = ({ items }) => (
    <div className="space-y-2">
      {items.map((item, idx) => (
        <div key={idx} className="bg-white p-3 rounded shadow-sm">
          {item}
        </div>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Student Performance Analysis Dashboard
        </h1>

        {/* Charts Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <MetricCard title="Performance Timeline">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={dashboardData.timelineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="accuracy" stroke="#4CAF50" name="Accuracy %" strokeWidth={2} />
                <Line type="monotone" dataKey="mistakesCorrected" stroke="#2196F3" name="Mistakes Corrected" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </MetricCard>

          <MetricCard title="Topic Performance">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={dashboardData.topicPerformance}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="accuracy" fill="#4CAF50" name="Accuracy %" />
              </BarChart>
            </ResponsiveContainer>
          </MetricCard>
        </div>

        {/* Performance Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Strengths Card */}
          <MetricCard title="Strengths">
            <ListCard items={dashboardData.performance_labels.strengths} />
          </MetricCard>

          {/* Challenges Card */}
          <MetricCard title="Challenges">
            <ListCard items={dashboardData.performance_labels.challenges} />
          </MetricCard>

          {/* Recommendations Card */}
          <MetricCard title="Recommendations">
            <ListCard items={dashboardData.recommendations.priority_actions} />
          </MetricCard>
        </div>

        {/* Student Profile Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Key Traits Card */}
          <MetricCard title="Key Traits">
            <ListCard items={dashboardData.persona.key_traits} />
          </MetricCard>

          {/* Learning Style Card */}
          <MetricCard title="Learning Style">
            <ListCard items={dashboardData.persona.learning_style} />
          </MetricCard>
        </div>

        {/* Distribution Charts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <MetricCard title="Topic Distribution">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={[
                    { name: 'Strong Topics', value: dashboardData.insights.topics.strong.length },
                    { name: 'Weak Topics', value: dashboardData.insights.topics.weak.length },
                    { name: 'Practice Needed', value: dashboardData.insights.topics.needs_practice.length }
                  ]}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label={({name, percent}) => `${name}: ${(percent * 100).toFixed(0)}%`}
                >
                  {({ data }) => data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </MetricCard>

          <MetricCard title="Performance Overview">
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart 
                cx="50%" 
                cy="50%" 
                outerRadius="80%" 
                data={[
                  { subject: 'Accuracy', value: dashboardData.insights.trending.recent_accuracy * 100 },
                  { subject: 'Improvement', value: dashboardData.insights.trending.improvement ? 80 : 40 },
                  { subject: 'Corrections', value: (dashboardData.insights.learning.recent_corrections / 5) * 100 }
                ]}
              >
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <Radar name="Performance" dataKey="value" stroke="#4CAF50" fill="#4CAF50" fillOpacity={0.6} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </MetricCard>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;