'use client';

import { User, Briefcase, Code, Target, TrendingUp } from 'lucide-react';

interface SummaryCardProps {
  summary: {
    professional_summary: string;
    career_highlights: string[];
    top_strengths: string[];
    potential_weaknesses: string[];
    career_level: string;
    primary_technology_stack: string[];
    suggested_job_roles: string[];
    suggested_industries: string[];
    top_keywords: string[];
  };
}

export function SummaryCard({ summary }: SummaryCardProps) {
  return (
    <div className="border rounded-xl p-6 space-y-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
        AI-Generated Summary
      </h3>

      <div className="space-y-4">
        <div className="flex items-start space-x-3">
          <User className="w-5 h-5 text-blue-500 mt-0.5" />
          <div className="flex-1">
            <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Professional Summary</h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">{summary.professional_summary}</p>
          </div>
        </div>

        {summary.career_highlights.length > 0 && (
          <div className="flex items-start space-x-3">
            <TrendingUp className="w-5 h-5 text-green-500 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Career Highlights</h4>
              <ul className="space-y-1">
                {summary.career_highlights.map((highlight, index) => (
                  <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                    <span className="mr-2">•</span>
                    <span>{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        <div className="flex items-start space-x-3">
          <Briefcase className="w-5 h-5 text-purple-500 mt-0.5" />
          <div className="flex-1">
            <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Career Level</h4>
            <span className="px-3 py-1 text-sm bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300 rounded-full">
              {summary.career_level}
            </span>
          </div>
        </div>

        {summary.primary_technology_stack.length > 0 && (
          <div className="flex items-start space-x-3">
            <Code className="w-5 h-5 text-blue-500 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Technology Stack</h4>
              <div className="flex flex-wrap gap-2">
                {summary.primary_technology_stack.map((tech, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 text-sm bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 rounded-full"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {summary.suggested_job_roles.length > 0 && (
          <div className="flex items-start space-x-3">
            <Target className="w-5 h-5 text-green-500 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Suggested Job Roles</h4>
              <div className="flex flex-wrap gap-2">
                {summary.suggested_job_roles.map((role, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 text-sm bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 rounded-full"
                  >
                    {role}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {summary.suggested_industries.length > 0 && (
          <div className="flex items-start space-x-3">
            <Target className="w-5 h-5 text-orange-500 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Suggested Industries</h4>
              <div className="flex flex-wrap gap-2">
                {summary.suggested_industries.map((industry, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 text-sm bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300 rounded-full"
                  >
                    {industry}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {summary.top_keywords.length > 0 && (
          <div className="flex items-start space-x-3">
            <Code className="w-5 h-5 text-gray-500 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Top Keywords for ATS</h4>
              <div className="flex flex-wrap gap-2">
                {summary.top_keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 text-sm bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300 rounded-full"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
