'use client';

import { ArrowRight, Check, X } from 'lucide-react';
import { ResumeChange } from '@/hooks/api/accelerator';

interface ResumeDiffViewerProps {
  changes: ResumeChange[];
  title: string;
}

export function ResumeDiffViewer({ changes, title }: ResumeDiffViewerProps) {
  if (changes.length === 0) {
    return (
      <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{title}</h3>
        <p className="text-gray-600 dark:text-gray-400 text-center">No changes made</p>
      </div>
    );
  }

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{title}</h3>
      <div className="space-y-4">
        {changes.map((change, index) => (
          <div key={index} className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-start space-x-3 mb-3">
              <div className="flex-shrink-0 w-8 h-8 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center">
                <X className="w-4 h-4 text-red-600 dark:text-red-400" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Original</p>
                <p className="text-gray-900 dark:text-gray-100 line-through opacity-70">{change.original}</p>
              </div>
            </div>

            <div className="flex items-center justify-center my-2">
              <ArrowRight className="w-5 h-5 text-gray-400" />
            </div>

            <div className="flex items-start space-x-3 mb-3">
              <div className="flex-shrink-0 w-8 h-8 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center">
                <Check className="w-4 h-4 text-green-600 dark:text-green-400" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Optimized</p>
                <p className="text-gray-900 dark:text-gray-100 font-medium">{change.optimized}</p>
              </div>
            </div>

            <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700 space-y-2">
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Reason for Change</p>
                <p className="text-sm text-gray-700 dark:text-gray-300">{change.reason}</p>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">ATS Improvement</p>
                  <p className="text-sm text-blue-600 dark:text-blue-400">{change.ats_improvement}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Recruiter Impact</p>
                  <p className="text-sm text-purple-600 dark:text-purple-400">{change.recruiter_impact}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
