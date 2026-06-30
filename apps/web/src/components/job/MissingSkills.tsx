'use client';

import { AlertTriangle, Clock, BookOpen, ExternalLink } from 'lucide-react';

interface MissingSkillsProps {
  missingSkills: Array<{
    skill_name: string;
    category: string;
    learning_priority: string;
    estimated_learning_time?: string;
    difficulty?: string;
    free_resources: string[];
  }>;
}

export function MissingSkills({ missingSkills }: MissingSkillsProps) {
  const getCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'critical':
        return 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300';
      case 'recommended':
        return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300';
      case 'bonus':
        return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300';
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'text-red-600 dark:text-red-400';
      case 'medium':
        return 'text-yellow-600 dark:text-yellow-400';
      case 'low':
        return 'text-green-600 dark:text-green-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  const getDifficultyColor = (difficulty?: string) => {
    if (!difficulty) return 'text-gray-600 dark:text-gray-400';
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

  if (missingSkills.length === 0) {
    return (
      <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
        <div className="flex items-center space-x-3 mb-4">
          <AlertTriangle className="w-6 h-6 text-green-600 dark:text-green-400" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Missing Skills
          </h3>
        </div>
        <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
          <p className="text-green-700 dark:text-green-400">
            Great! You have all the required skills for this position.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-6">
        <AlertTriangle className="w-6 h-6 text-orange-600 dark:text-orange-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Missing Skills ({missingSkills.length})
        </h3>
      </div>

      <div className="space-y-4">
        {missingSkills.map((skill, index) => (
          <div
            key={index}
            className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <h4 className="font-medium text-gray-900 dark:text-gray-100">
                    {skill.skill_name}
                  </h4>
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryColor(
                      skill.category
                    )}`}
                  >
                    {skill.category}
                  </span>
                </div>
                <div className="flex items-center space-x-4 text-sm">
                  {skill.estimated_learning_time && (
                    <div className="flex items-center space-x-1">
                      <Clock className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                      <span className="text-gray-600 dark:text-gray-400">
                        {skill.estimated_learning_time}
                      </span>
                    </div>
                  )}
                  {skill.difficulty && (
                    <div className="flex items-center space-x-1">
                      <span className={`font-medium ${getDifficultyColor(skill.difficulty)}`}>
                        {skill.difficulty}
                      </span>
                    </div>
                  )}
                  <div className="flex items-center space-x-1">
                    <span className={`font-medium ${getPriorityColor(skill.learning_priority)}`}>
                      Priority: {skill.learning_priority}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {skill.free_resources && skill.free_resources.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-2 mb-2">
                  <BookOpen className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Learning Resources
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {skill.free_resources.map((resource, idx) => (
                    <span
                      key={idx}
                      className="flex items-center space-x-1 px-2 py-1 text-xs bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300 rounded"
                    >
                      <ExternalLink className="w-3 h-3" />
                      <span>{resource}</span>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
        <p className="text-sm text-blue-700 dark:text-blue-400">
          <strong>Tip:</strong> Focus on critical skills first. Consider creating projects to demonstrate
          these skills on your resume.
        </p>
      </div>
    </div>
  );
}
