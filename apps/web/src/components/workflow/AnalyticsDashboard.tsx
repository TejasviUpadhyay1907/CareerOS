'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface AnalyticsDashboardProps {
  metrics: {
    application_funnel: Record<string, number>;
    success_rate: number;
    response_rate: number;
    interview_conversion: number;
    offer_conversion: number;
    technology_trends: Record<string, number>;
    most_successful_resume?: any;
    most_successful_category?: string;
    most_requested_skills: string[];
    weak_areas: string[];
  };
}

export function AnalyticsDashboard({ metrics }: AnalyticsDashboardProps) {
  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

  const funnelData = Object.entries(metrics.application_funnel).map(([stage, count]) => ({
    name: stage.replace('_', ' '),
    value: count,
  }));

  const technologyData = Object.entries(metrics.technology_trends).map(([tech, count]) => ({
    name: tech,
    value: count,
  }));

  const skillData = metrics.most_requested_skills.map((skill, index) => ({
    name: skill,
    value: 100 - index * 10, // Simulated value
  }));

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard title="Success Rate" value={`${(metrics.success_rate * 100).toFixed(1)}%`} color="green" />
        <MetricCard title="Response Rate" value={`${(metrics.response_rate * 100).toFixed(1)}%`} color="blue" />
        <MetricCard title="Interview Conversion" value={`${(metrics.interview_conversion * 100).toFixed(1)}%`} color="purple" />
        <MetricCard title="Offer Conversion" value={`${(metrics.offer_conversion * 100).toFixed(1)}%`} color="yellow" />
      </div>

      {/* Application Funnel */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Application Funnel</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={funnelData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis dataKey="name" stroke="#6B7280" />
            <YAxis stroke="#6B7280" />
            <Tooltip />
            <Bar dataKey="value" fill="#3B82F6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Technology Trends */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Technology Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={technologyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis dataKey="name" stroke="#6B7280" />
              <YAxis stroke="#6B7280" />
              <Tooltip />
              <Bar dataKey="value" fill="#10B981" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Most Requested Skills */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Most Requested Skills</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={skillData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => entry.name}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {skillData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Top Insights</h3>
          <div className="space-y-3">
            {metrics.most_successful_category && (
              <div className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                <span className="text-sm text-gray-700 dark:text-gray-300">Most Successful Category</span>
                <span className="font-medium text-green-600 dark:text-green-400">{metrics.most_successful_category}</span>
              </div>
            )}
            <div className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <span className="text-sm text-gray-700 dark:text-gray-300">Total Applications</span>
              <span className="font-medium text-blue-600 dark:text-blue-400">
                {Object.values(metrics.application_funnel).reduce((a, b) => a + b, 0)}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Areas to Improve</h3>
          <div className="space-y-2">
            {metrics.weak_areas.length === 0 ? (
              <p className="text-sm text-gray-500 dark:text-gray-400">No weak areas identified</p>
            ) : (
              metrics.weak_areas.map((area, index) => (
                <div key={index} className="flex items-center space-x-2 p-2 bg-red-50 dark:bg-red-900/20 rounded-lg">
                  <span className="text-sm text-red-600 dark:text-red-400">•</span>
                  <span className="text-sm text-gray-700 dark:text-gray-300">{area}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

interface MetricCardProps {
  title: string;
  value: string;
  color: string;
}

function MetricCard({ title, value, color }: MetricCardProps) {
  const colorClasses = {
    green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
    purple: 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400',
    yellow: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400',
  };

  return (
    <div className={`${colorClasses[color as keyof typeof colorClasses]} rounded-xl p-4`}>
      <p className="text-sm font-medium mb-1">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}
