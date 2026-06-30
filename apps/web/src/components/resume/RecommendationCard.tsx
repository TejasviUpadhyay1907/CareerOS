'use client';

import { Lightbulb, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface RecommendationCardProps {
  recommendations: string[];
  strengths: string[];
  weaknesses: string[];
  missingSections: string[];
}

export function RecommendationCard({
  recommendations,
  strengths,
  weaknesses,
  missingSections,
}: RecommendationCardProps) {
  return (
    <div className="border rounded-xl p-6 space-y-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
        Insights & Recommendations
      </h3>

      {recommendations.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <Lightbulb className="w-5 h-5 text-yellow-500" />
            <h4 className="font-medium text-gray-700 dark:text-gray-300">Recommendations</h4>
          </div>
          <ul className="space-y-2">
            {recommendations.map((rec, index) => (
              <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                <span className="mr-2 text-yellow-500">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {strengths.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-5 h-5 text-green-500" />
            <h4 className="font-medium text-gray-700 dark:text-gray-300">Strengths</h4>
          </div>
          <ul className="space-y-2">
            {strengths.map((strength, index) => (
              <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                <span className="mr-2 text-green-500">✓</span>
                <span>{strength}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {weaknesses.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <h4 className="font-medium text-gray-700 dark:text-gray-300">Areas for Improvement</h4>
          </div>
          <ul className="space-y-2">
            {weaknesses.map((weakness, index) => (
              <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                <span className="mr-2 text-red-500">!</span>
                <span>{weakness}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {missingSections.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-orange-500" />
            <h4 className="font-medium text-gray-700 dark:text-gray-300">Missing Sections</h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {missingSections.map((section, index) => (
              <span
                key={index}
                className="px-3 py-1 text-sm bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300 rounded-full"
              >
                {section}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
