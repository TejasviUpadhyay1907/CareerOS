'use client';

import { TrendingUp, AlertCircle, CheckCircle2 } from 'lucide-react';

interface HealthScoreCardProps {
  score: number;
  breakdown: Record<string, number>;
}

export function HealthScoreCard({ score, breakdown }: HealthScoreCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400';
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-100 dark:bg-green-900';
    if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900';
    return 'bg-red-100 dark:bg-red-900';
  };

  const getProgressColor = (score: number) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const categoryLabels: Record<string, string> = {
    formatting: 'Formatting',
    readability: 'Readability',
    action_verbs: 'Action Verbs',
    quantified_impact: 'Quantified Impact',
    skills_coverage: 'Skills Coverage',
    project_quality: 'Project Quality',
    experience_quality: 'Experience Quality',
    education: 'Education',
    ats_friendliness: 'ATS Friendliness',
    completeness: 'Completeness',
  };

  return (
    <div className="border rounded-xl p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Resume Health Score
        </h3>
        <div className={`px-3 py-1 rounded-full ${getScoreBg(score)} ${getScoreColor(score)}`}>
          <span className="text-sm font-semibold">{score}/100</span>
        </div>
      </div>

      <div className="flex items-center justify-center py-8">
        <div className="relative">
          <svg className="w-32 h-32 transform -rotate-90">
            <circle
              cx="64"
              cy="64"
              r="56"
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              className="text-gray-200 dark:text-gray-700"
            />
            <circle
              cx="64"
              cy="64"
              r="56"
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              strokeDasharray={`${2 * Math.PI * 56}`}
              strokeDashoffset={`${2 * Math.PI * 56 * (1 - score / 100)}`}
              className={getScoreColor(score).replace('text-', 'stroke-')}
              strokeLinecap="round"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className={`text-3xl font-bold ${getScoreColor(score)}`}>{score}</span>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Score Breakdown
        </h4>
        <div className="space-y-3">
          {Object.entries(breakdown).map(([key, value]) => (
            <div key={key} className="space-y-1">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">
                  {categoryLabels[key] || key}
                </span>
                <span className={`font-medium ${getScoreColor(value)}`}>{value}</span>
              </div>
              <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div
                  className={`h-full ${getProgressColor(value)} transition-all duration-500`}
                  style={{ width: `${value}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
          <TrendingUp className="w-4 h-4" />
          <span>Your resume is {score >= 80 ? 'in excellent shape' : score >= 60 ? 'good but can be improved' : 'needs significant improvement'}</span>
        </div>
      </div>
    </div>
  );
}
