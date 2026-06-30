'use client';

import { Heart, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { HealthScore } from '@/hooks/api/career';

interface CareerHealthCardProps {
  healthScore: HealthScore;
}

export function CareerHealthCard({ healthScore }: CareerHealthCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600 dark:text-green-400';
    if (score >= 70) return 'text-blue-600 dark:text-blue-400';
    if (score >= 50) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 90) return 'bg-green-100 dark:bg-green-900/20';
    if (score >= 70) return 'bg-blue-100 dark:bg-blue-900/20';
    if (score >= 50) return 'bg-yellow-100 dark:bg-yellow-900/20';
    return 'bg-red-100 dark:bg-red-900/20';
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-5 h-5 text-green-600 dark:text-green-400" />;
      case 'down':
        return <TrendingDown className="w-5 h-5 text-red-600 dark:text-red-400" />;
      default:
        return <Minus className="w-5 h-5 text-gray-600 dark:text-gray-400" />;
    }
  };

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Heart className="w-6 h-6 text-red-600 dark:text-red-400" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Career Health Score
          </h3>
        </div>
        <div className="flex items-center space-x-2">
          {getTrendIcon(healthScore.trend)}
          <span className="text-sm text-gray-600 dark:text-gray-400 capitalize">
            {healthScore.trend}
          </span>
        </div>
      </div>

      {/* Overall Score */}
      <div className={`p-6 rounded-xl ${getScoreBgColor(healthScore.overall_score)} mb-6`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Overall Score</p>
            <p className={`text-5xl font-bold ${getScoreColor(healthScore.overall_score)}`}>
              {healthScore.overall_score}
            </p>
            <p className={`text-lg font-medium mt-2 ${getScoreColor(healthScore.overall_score)}`}>
              Grade: {healthScore.grade}
            </p>
          </div>
          <div className="w-32 h-32 rounded-full border-8 flex items-center justify-center">
            <span className={`text-2xl font-bold ${getScoreColor(healthScore.overall_score)}`}>
              {healthScore.overall_score}%
            </span>
          </div>
        </div>
      </div>

      {/* Breakdown */}
      <div className="space-y-3">
        <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-4">Score Breakdown</h4>
        {Object.entries(healthScore.breakdown).map(([category, data]) => (
          <div key={category} className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
                {category.replace(/_/g, ' ')}
              </span>
              <div className="flex items-center space-x-2">
                <span className={`text-sm font-semibold ${getScoreColor(data.score)}`}>
                  {data.score}%
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  ({data.weight}% weight)
                </span>
              </div>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-500 ${
                  data.score >= 70
                    ? 'bg-green-500'
                    : data.score >= 50
                    ? 'bg-yellow-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${data.score}%` }}
              />
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400">{data.reasoning}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
