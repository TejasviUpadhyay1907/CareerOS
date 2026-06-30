'use client';

import { Brain, TrendingUp, AlertTriangle, CheckCircle2, Target, Clock, MessageSquare } from 'lucide-react';
import { Application } from '@/hooks/api/workflow';

interface ApplicationInsightsProps {
  application: Application;
  aiInsights: {
    next_best_action?: string;
    urgency?: string;
    probability_of_success?: number;
    recommended_followup?: string;
    suggested_message?: string;
    interview_countdown?: number;
    preparation_progress?: number;
    ats_score?: number;
  };
}

export function ApplicationInsights({ application, aiInsights }: ApplicationInsightsProps) {
  const getUrgencyColor = (urgency?: string) => {
    switch (urgency) {
      case 'high':
        return 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400';
      case 'medium':
        return 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400';
      case 'low':
        return 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400';
      default:
        return 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400';
    }
  };

  const getProbabilityColor = (probability?: number) => {
    if (!probability) return 'text-gray-600 dark:text-gray-400';
    if (probability >= 80) return 'text-green-600 dark:text-green-400';
    if (probability >= 60) return 'text-blue-600 dark:text-blue-400';
    if (probability >= 40) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center space-x-2 mb-4">
        <Brain className="w-5 h-5 text-purple-600 dark:text-purple-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">AI Insights</h3>
      </div>

      {/* Next Best Action */}
      {aiInsights.next_best_action && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg p-4 border border-purple-200 dark:border-purple-800">
          <div className="flex items-start space-x-3">
            <Target className="w-5 h-5 text-purple-600 dark:text-purple-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-1">Next Best Action</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">{aiInsights.next_best_action}</p>
            </div>
          </div>
        </div>
      )}

      {/* Key Metrics */}
      <div className="grid grid-cols-2 gap-3">
        {aiInsights.urgency && (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-2 mb-1">
              <AlertTriangle className="w-4 h-4 text-gray-600 dark:text-gray-400" />
              <span className="text-xs text-gray-600 dark:text-gray-400">Urgency</span>
            </div>
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getUrgencyColor(aiInsights.urgency)}`}>
              {aiInsights.urgency}
            </span>
          </div>
        )}

        {aiInsights.probability_of_success !== undefined && (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-2 mb-1">
              <TrendingUp className="w-4 h-4 text-gray-600 dark:text-gray-400" />
              <span className="text-xs text-gray-600 dark:text-gray-400">Success Probability</span>
            </div>
            <span className={`text-lg font-bold ${getProbabilityColor(aiInsights.probability_of_success)}`}>
              {aiInsights.probability_of_success}%
            </span>
          </div>
        )}

        {aiInsights.ats_score !== undefined && (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-2 mb-1">
              <CheckCircle2 className="w-4 h-4 text-gray-600 dark:text-gray-400" />
              <span className="text-xs text-gray-600 dark:text-gray-400">ATS Score</span>
            </div>
            <span className="text-lg font-bold text-blue-600 dark:text-blue-400">
              {aiInsights.ats_score}%
            </span>
          </div>
        )}

        {aiInsights.interview_countdown !== undefined && (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-2 mb-1">
              <Clock className="w-4 h-4 text-gray-600 dark:text-gray-400" />
              <span className="text-xs text-gray-600 dark:text-gray-400">Interview Countdown</span>
            </div>
            <span className="text-lg font-bold text-purple-600 dark:text-purple-400">
              {aiInsights.interview_countdown} days
            </span>
          </div>
        )}
      </div>

      {/* Recommended Follow-up */}
      {aiInsights.recommended_followup && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-start space-x-3">
            <MessageSquare className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Recommended Follow-up</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">{aiInsights.recommended_followup}</p>
            </div>
          </div>
        </div>
      )}

      {/* Suggested Message */}
      {aiInsights.suggested_message && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-start space-x-3">
            <MessageSquare className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Suggested Message</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400 italic">&quot;{aiInsights.suggested_message}&quot;</p>
            </div>
          </div>
        </div>
      )}

      {/* Preparation Progress */}
      {aiInsights.preparation_progress !== undefined && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-medium text-gray-900 dark:text-gray-100">Preparation Progress</h4>
            <span className="text-sm text-gray-600 dark:text-gray-400">{aiInsights.preparation_progress}%</span>
          </div>
          <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all"
              style={{ width: `${aiInsights.preparation_progress}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
