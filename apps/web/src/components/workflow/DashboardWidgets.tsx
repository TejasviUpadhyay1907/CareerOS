'use client';

import { Briefcase, Clock, Bell, TrendingUp, Target, CheckCircle2 } from 'lucide-react';
import { DashboardData } from '@/hooks/api/workflow';

interface DashboardWidgetsProps {
  dashboardData: DashboardData;
}

export function DashboardWidgets({ dashboardData }: DashboardWidgetsProps) {
  const { metrics, morning_brief } = dashboardData;

  return (
    <div className="space-y-6">
      {/* Morning Brief */}
      {morning_brief && (
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-6 text-white">
          <h2 className="text-2xl font-bold mb-2">{morning_brief.greeting}!</h2>
          <p className="text-blue-100 mb-4">Here&apos;s your career brief for today</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white/20 backdrop-blur rounded-lg p-4">
              <p className="text-sm text-blue-100 mb-2">Today&apos;s Priorities</p>
              <p className="text-3xl font-bold">{morning_brief.today_priorities.length}</p>
            </div>
            <div className="bg-white/20 backdrop-blur rounded-lg p-4">
              <p className="text-sm text-blue-100 mb-2">Upcoming Interviews</p>
              <p className="text-3xl font-bold">{morning_brief.upcoming_interviews.length}</p>
            </div>
            <div className="bg-white/20 backdrop-blur rounded-lg p-4">
              <p className="text-sm text-blue-100 mb-2">Deadlines Today</p>
              <p className="text-3xl font-bold">{morning_brief.deadlines_today.length}</p>
            </div>
          </div>
        </div>
      )}

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          icon={<Briefcase className="w-5 h-5" />}
          title="Total Applications"
          value={metrics.total_applications}
          color="blue"
        />
        <MetricCard
          icon={<Clock className="w-5 h-5" />}
          title="Pending Tasks"
          value={metrics.pending_tasks}
          color="yellow"
        />
        <MetricCard
          icon={<Bell className="w-5 h-5" />}
          title="Unread Notifications"
          value={metrics.unread_notifications}
          color="red"
        />
        <MetricCard
          icon={<TrendingUp className="w-5 h-5" />}
          title="Response Rate"
          value={`${(metrics.response_rate * 100).toFixed(1)}%`}
          color="green"
        />
      </div>

      {/* Applications by Stage */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Applications by Stage
        </h3>
        <div className="space-y-3">
          {Object.entries(metrics.applications_by_stage).map(([stage, count]) => (
            <div key={stage} className="flex items-center justify-between">
              <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">
                {stage.replace('_', ' ')}
              </span>
              <div className="flex items-center space-x-2">
                <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500 rounded-full"
                    style={{ width: `${(count / metrics.total_applications) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100 w-8 text-right">
                  {count}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Conversion Rates */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ConversionCard
          icon={<Target className="w-5 h-5" />}
          title="Interview Rate"
          value={`${(metrics.interview_rate * 100).toFixed(1)}%`}
          color="blue"
        />
        <ConversionCard
          icon={<CheckCircle2 className="w-5 h-5" />}
          title="Offer Rate"
          value={`${(metrics.offer_rate * 100).toFixed(1)}%`}
          color="green"
        />
        <ConversionCard
          icon={<TrendingUp className="w-5 h-5" />}
          title="Success Rate"
          value={`${(metrics.response_rate * 100).toFixed(1)}%`}
          color="purple"
        />
      </div>
    </div>
  );
}

interface MetricCardProps {
  icon: React.ReactNode;
  title: string;
  value: string | number;
  color: string;
}

function MetricCard({ icon, title, value, color }: MetricCardProps) {
  const colorClasses = {
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
    yellow: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400',
    red: 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400',
    green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
    purple: 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400',
  };

  return (
    <div className={`${colorClasses[color as keyof typeof colorClasses]} rounded-xl p-4`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium">{title}</span>
        {icon}
      </div>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}

interface ConversionCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  color: string;
}

function ConversionCard({ icon, title, value, color }: ConversionCardProps) {
  const colorClasses = {
    blue: 'border-blue-200 dark:border-blue-800',
    green: 'border-green-200 dark:border-green-800',
    purple: 'border-purple-200 dark:border-purple-800',
  };

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-xl p-4 border ${colorClasses[color as keyof typeof colorClasses]}`}>
      <div className="flex items-center space-x-3 mb-2">
        <div className="p-2 bg-gray-100 dark:bg-gray-700 rounded-lg">{icon}</div>
        <span className="text-sm text-gray-600 dark:text-gray-400">{title}</span>
      </div>
      <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{value}</p>
    </div>
  );
}
