import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import StudentDashboard from './components/StudentDashboard';

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <StudentDashboard />
  </React.StrictMode>
);