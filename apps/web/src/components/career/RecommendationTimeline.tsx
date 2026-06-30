'use client';

import { Lightbulb, Clock, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';
import { Recommendation } from '@/hooks/api/career';

interface RecommendationTimelineProps {
  recommendations: Recommendation[];
  onUpdateStatus: (id: string, status: string, userStatus: string) => void;
}

export function RecommendationTimeline({ recommendations, onUpdateStatus }: RecommendationTimelineProps) {
  const getCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'immediate':
        return 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300';
      case 'this_week':
        return 'bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300';
      case 'this_month':
        return 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300';
      case 'long_term':
        return 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300';
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical':
        return <AlertCircle className="w-4 h-4 text-red-600 dark:text-red-400" />;
      case 'high':
        return <AlertCircle className="w-4 h-4 text-orange-600 dark:text-orange-400" />;
      case 'medium':
        return <Clock className="w-4 h-4 text-yellow-600 dark:text-yellow-400" />;
      case 'low':
        return <Lightbulb className="w-4 h-4 text-blue-600 dark:text-blue-400" />;
      default:
        return <Lightbulb className="w-4 h-4 text-gray-600 dark:text-gray-400" />;
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'hard':
        return 'text-red-600 dark:text-red-400';
      case 'medium':
        return 'text-yellow-600 dark:text-yellow-400';
      case 'easy':
        return 'text-green-600 dark:text-green-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  if (recommendations.length === 0) {
    return (
      <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
        <div className="flex items-center space-x-3 mb-4">
          <Lightbulb className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            AI Recommendations
          </h3>
        </div>
        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <p className="text-gray-600 dark:text-gray-400 text-center">
            No recommendations yet. Upload a resume and analyze jobs to get personalized recommendations.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-6">
        <Lightbulb className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          AI Recommendations
        </h3>
        <span className="px-2 py-1 text-xs bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 rounded-full">
          {recommendations.length}
        </span>
      </div>

      <div className="space-y-4">
        {recommendations.map((rec) => (
          <div
            key={rec.id}
            className={`p-4 border rounded-lg transition-all ${
              rec.user_status === 'completed'
                ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                : rec.user_status === 'dismissed'
                ? 'bg-gray-50 dark:bg-gray-700/50 border-gray-200 dark:border-gray-700 opacity-60'
                : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:shadow-md'
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  {getPriorityIcon(rec.priority)}
                  <h4 className="font-medium text-gray-900 dark:text-gray-100">
                    {rec.title}
                  </h4>
                  <span className={`px-2 py-1 text-xs rounded-full ${getCategoryColor(rec.category)}`}>
                    {rec.category.replace('_', ' ')}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  {rec.description}
                </p>
                <div className="flex flex-wrap gap-2 text-xs">
                  <span className={`px-2 py-1 rounded ${getDifficultyColor(rec.difficulty)}`}>
                    {rec.difficulty}
                  </span>
                  <span className="px-2 py-1 bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300 rounded">
                    {rec.estimated_time}
                  </span>
                  <span className="px-2 py-1 bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 rounded">
                    {Math.round(rec.confidence)}% confidence
                  </span>
                </div>
              </div>
              <div className="flex items-center space-x-2 ml-4">
                {rec.user_status === 'completed' ? (
                  <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />
                ) : rec.user_status === 'dismissed' ? (
                  <XCircle className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                ) : (
                  <div className="flex space-x-1">
                    <button
                      onClick={() => onUpdateStatus(rec.id, 'completed', 'completed')}
                      className="p-2 hover:bg-green-100 dark:hover:bg-green-900 rounded-full transition-colors"
                      title="Mark as completed"
                    >
                      <CheckCircle2 className="w-4 h-4 text-green-600 dark:text-green-400" />
                    </button>
                    <button
                      onClick={() => onUpdateStatus(rec.id, 'dismissed', 'dismissed')}
                      className="p-2 hover:bg-red-100 dark:hover:bg-red-900 rounded-full transition-colors"
                      title="Dismiss"
                    >
                      <XCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                    </button>
                  </div>
                )}
              </div>
            </div>

            {rec.evidence && rec.evidence.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Evidence:</p>
                <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                  {rec.evidence.slice(0, 3).map((evidence, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="mr-2 text-gray-400">•</span>
                      <span>{evidence}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {rec.expected_benefit && (
              <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                <p className="text-xs text-green-600 dark:text-green-400">
                  <strong>Expected Benefit:</strong> {rec.expected_benefit}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
