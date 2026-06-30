'use client';

import { FileText, Zap, TrendingUp, Target } from 'lucide-react';
import { ResumeOptimization } from '@/hooks/api/accelerator';

interface OptimizationDashboardProps {
  optimization: ResumeOptimization;
}

export function OptimizationDashboard({ optimization }: OptimizationDashboardProps) {
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

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-6">
        <Zap className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Resume Optimization Results
        </h3>
      </div>

      {/* Optimization Score */}
      <div className={`p-6 rounded-xl ${getScoreBgColor(optimization.optimization_score)} mb-6`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Optimization Score</p>
            <p className={`text-5xl font-bold ${getScoreColor(optimization.optimization_score)}`}>
              {optimization.optimization_score}
            </p>
          </div>
          <div className="w-32 h-32 rounded-full border-8 flex items-center justify-center">
            <span className={`text-2xl font-bold ${getScoreColor(optimization.optimization_score)}`}>
              {optimization.optimization_score}%
            </span>
          </div>
        </div>
      </div>

      {/* Impact Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
          <div className="flex items-center space-x-2 mb-2">
            <Target className="w-5 h-5 text-green-600 dark:text-green-400" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">ATS Improvement</span>
          </div>
          <p className="text-2xl font-bold text-green-600 dark:text-green-400">
            +{optimization.estimated_ats_improvement}%
          </p>
        </div>
        <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="flex items-center space-x-2 mb-2">
            <TrendingUp className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Match Increase</span>
          </div>
          <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            +{optimization.estimated_match_increase}%
          </p>
        </div>
        <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
          <div className="flex items-center space-x-2 mb-2">
            <FileText className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Interview Probability</span>
          </div>
          <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
            +{optimization.estimated_interview_probability}%
          </p>
        </div>
      </div>

      {/* Optimized Summary */}
      {optimization.optimized_summary && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Optimized Summary</h4>
          <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <p className="text-gray-700 dark:text-gray-300">{optimization.optimized_summary}</p>
          </div>
        </div>
      )}

      {/* Changes Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <p className="text-sm text-gray-600 dark:text-gray-400">Experience Changes</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {optimization.optimized_experience.length}
          </p>
        </div>
        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <p className="text-sm text-gray-600 dark:text-gray-400">Project Changes</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {optimization.optimized_projects.length}
          </p>
        </div>
        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <p className="text-sm text-gray-600 dark:text-gray-400">Keyword Additions</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {optimization.keyword_additions.length}
          </p>
        </div>
        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <p className="text-sm text-gray-600 dark:text-gray-400">Skills Reordered</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {optimization.optimized_skills.optimized_order.length}
          </p>
        </div>
      </div>
    </div>
  );
}
