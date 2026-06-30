'use client';

import { Sun, Calendar, Target } from 'lucide-react';
import { TodayPriority } from '@/hooks/api/career';

interface MorningBriefProps {
  greeting: string;
  todaysPriorities: TodayPriority[];
}

export function MorningBrief({ greeting, todaysPriorities }: MorningBriefProps) {
  return (
    <div className="border rounded-xl p-6 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-900">
      <div className="flex items-center space-x-3 mb-6">
        <Sun className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          {greeting}
        </h3>
      </div>

      <div className="mb-6">
        <p className="text-gray-700 dark:text-gray-300">
          Here are your top priorities for today to advance your career:
        </p>
      </div>

      {todaysPriorities.length > 0 ? (
        <div className="space-y-4">
          {todaysPriorities.map((priority, index) => (
            <div
              key={index}
              className="p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 dark:text-blue-400 font-semibold text-sm">
                    {index + 1}
                  </span>
                </div>
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-1">
                    {priority.title}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    {priority.description}
                  </p>
                  <div className="flex items-center space-x-4 text-xs">
                    <div className="flex items-center space-x-1">
                      <Calendar className="w-3 h-3 text-gray-500 dark:text-gray-400" />
                      <span className="text-gray-500 dark:text-gray-400">
                        {priority.estimated_time}
                      </span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Target className="w-3 h-3 text-gray-500 dark:text-gray-400" />
                      <span className="text-gray-500 dark:text-gray-400">
                        {priority.expected_benefit}
                      </span>
                    </div>
                    <div className="px-2 py-1 bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 rounded-full">
                      {Math.round(priority.confidence)}% confidence
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <p className="text-gray-600 dark:text-gray-400 text-center">
            No priorities set for today. Upload a resume and analyze jobs to get personalized recommendations.
          </p>
        </div>
      )}
    </div>
  );
}
