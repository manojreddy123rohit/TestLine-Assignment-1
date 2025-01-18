import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  BarChart, Bar, PieChart, Pie, Cell, ResponsiveContainer
} from 'recharts';

const StudentDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  useEffect(() => {
    // Simulated data since we can't actually fetch in this environment
    setDashboardData({
      timelineData: [
        { date: '2025-01-17', accuracy: 90, mistakesCorrected: 9 },
        { date: '2025-01-16', accuracy: 100, mistakesCorrected: 3 },
        { date: '2025-01-15', accuracy: 96, mistakesCorrected: 11 },
        { date: '2025-01-14', accuracy: 90, mistakesCorrected: 1 },
        { date: '2025-01-13', accuracy: 31, mistakesCorrected: 0 }
      ],
      topicPerformance: [
        { name: 'Human Physiology', accuracy: 72 },
        { name: 'Reproductive Health', accuracy: 43 },
        { name: 'Human Reproduction', accuracy: 38 },
        { name: 'Inheritance', accuracy: 30 }
      ],
      insights: {
        topics: {
          strong: ['Human Physiology'],
          weak: ['Reproductive Health', 'Human Reproduction', 'Inheritance'],
          needs_practice: ['Reproductive Health', 'Human Reproduction', 'Inheritance']
        },
        trending: {
          overall_accuracy: 0.72,
          recent_accuracy: 0.85
        }
      }
    });
  }, []);

  if (!dashboardData) {
    return <div className="w-full h-screen flex items-center justify-center">Loading...</div>;
  }

  const { timelineData, topicPerformance, insights } = dashboardData;

  return (
    <div className="w-full max-w-6xl mx-auto p-4 space-y-8">
      <h1 className="text-2xl font-bold text-center mb-8">Student Performance Analysis Dashboard</h1>

      {/* Performance Timeline */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Performance Timeline</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={timelineData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="accuracy" stroke="#8884d8" name="Accuracy (%)" />
            <Line type="monotone" dataKey="mistakesCorrected" stroke="#82ca9d" name="Mistakes Corrected" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Topic Performance */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Topic Performance</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={topicPerformance}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="accuracy" fill="#8884d8" name="Accuracy (%)" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Strength and Weakness Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Topic Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Strong Topics', value: insights.topics.strong.length },
                  { name: 'Weak Topics', value: insights.topics.weak.length },
                  { name: 'Needs Practice', value: insights.topics.needs_practice.length }
                ]}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({name, percent}) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
              >
                {(entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                )}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Recent vs Overall Performance */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Performance Comparison</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart 
              data={[
                {
                  name: 'Overall',
                  accuracy: insights.trending.overall_accuracy * 100
                },
                {
                  name: 'Recent',
                  accuracy: insights.trending.recent_accuracy * 100
                }
              ]}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="accuracy" fill="#82ca9d" name="Accuracy (%)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;