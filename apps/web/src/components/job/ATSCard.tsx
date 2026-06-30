'use client';

import { FileText, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';

interface ATSCardProps {
  keywordCoverage: number;
  formattingCompatibility: number;
  actionVerbsScore: number;
  roleAlignment: number;
  missingKeywords: string[];
  resumeLengthScore: number;
  sectionCompleteness: number;
  optimizationPotential: number;
}

export function ATSCard({
  keywordCoverage,
  formattingCompatibility,
  actionVerbsScore,
  roleAlignment,
  missingKeywords,
  resumeLengthScore,
  sectionCompleteness,
  optimizationPotential,
}: ATSCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400';
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <CheckCircle2 className="w-4 h-4 text-green-600 dark:text-green-400" />;
    if (score >= 60) return <AlertTriangle className="w-4 h-4 text-yellow-600 dark:text-yellow-400" />;
    return <XCircle className="w-4 h-4 text-red-600 dark:text-red-400" />;
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-6">
        <FileText className="w-6 h-6 text-purple-600 dark:text-purple-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          ATS Analysis
        </h3>
      </div>

      {/* Overall ATS Score */}
      <div className="mb-6 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Overall ATS Score</p>
            <p className={`text-2xl font-bold ${getScoreColor(keywordCoverage)}`}>
              {keywordCoverage}%
            </p>
          </div>
          <div className="text-right">
            <p className={`text-sm font-medium ${getScoreColor(keywordCoverage)}`}>
              {getScoreLabel(keywordCoverage)}
            </p>
          </div>
        </div>
      </div>

      {/* Detailed Scores */}
      <div className="space-y-4 mb-6">
        <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <div className="flex items-center space-x-2">
            {getScoreIcon(keywordCoverage)}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Keyword Coverage
            </span>
          </div>
          <span className={`font-semibold ${getScoreColor(keywordCoverage)}`}>
            {keywordCoverage}%
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <div className="flex items-center space-x-2">
            {getScoreIcon(formattingCompatibility)}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Formatting
            </span>
          </div>
          <span className={`font-semibold ${getScoreColor(formattingCompatibility)}`}>
            {formattingCompatibility}%
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <div className="flex items-center space-x-2">
            {getScoreIcon(actionVerbsScore)}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Action Verbs
            </span>
          </div>
          <span className={`font-semibold ${getScoreColor(actionVerbsScore)}`}>
            {actionVerbsScore}%
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <div className="flex items-center space-x-2">
            {getScoreIcon(roleAlignment)}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Role Alignment
            </span>
          </div>
          <span className={`font-semibold ${getScoreColor(roleAlignment)}`}>
            {roleAlignment}%
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <div className="flex items-center space-x-2">
            {getScoreIcon(resumeLengthScore)}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Resume Length
            </span>
          </div>
          <span className={`font-semibold ${getScoreColor(resumeLengthScore)}`}>
            {resumeLengthScore}%
          </span>
        </div>

        <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <div className="flex items-center space-x-2">
            {getScoreIcon(sectionCompleteness)}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Section Completeness
            </span>
          </div>
          <span className={`font-semibold ${getScoreColor(sectionCompleteness)}`}>
            {sectionCompleteness}%
          </span>
        </div>
      </div>

      {/* Missing Keywords */}
      {missingKeywords.length > 0 && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <h4 className="font-medium text-red-700 dark:text-red-400 mb-2">
            Missing Keywords ({missingKeywords.length})
          </h4>
          <div className="flex flex-wrap gap-2">
            {missingKeywords.slice(0, 10).map((keyword, index) => (
              <span
                key={index}
                className="px-3 py-1 text-sm bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300 rounded-full"
              >
                {keyword}
              </span>
            ))}
            {missingKeywords.length > 10 && (
              <span className="px-3 py-1 text-sm bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300 rounded-full">
                +{missingKeywords.length - 10} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Optimization Potential */}
      <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
        <h4 className="font-medium text-blue-700 dark:text-blue-400 mb-2">
          Optimization Potential
        </h4>
        <div className="flex items-center space-x-2">
          <div className="flex-1 bg-blue-200 dark:bg-blue-800 rounded-full h-2">
            <div
              className="bg-blue-600 dark:bg-blue-400 h-2 rounded-full transition-all duration-500"
              style={{ width: `${optimizationPotential}%` }}
            />
          </div>
          <span className="text-sm font-semibold text-blue-700 dark:text-blue-400">
            {optimizationPotential}%
          </span>
        </div>
        <p className="mt-2 text-sm text-blue-600 dark:text-blue-400">
          {optimizationPotential >= 70
            ? 'Significant room for improvement'
            : optimizationPotential >= 40
            ? 'Moderate optimization possible'
            : 'Well optimized for ATS'}
        </p>
      </div>
    </div>
  );
}
