'use client';

import { BookOpen, Clock, Target, CheckCircle2 } from 'lucide-react';
import { InterviewKit } from '@/hooks/api/accelerator';

interface InterviewDashboardProps {
  kit: InterviewKit;
}

export function InterviewDashboard({ kit }: InterviewDashboardProps) {
  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-6">
        <BookOpen className="w-6 h-6 text-green-600 dark:text-green-400" />
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Interview Preparation Kit
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {kit.company_name} - {kit.role_title}
          </p>
        </div>
      </div>

      {/* Company & Role Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Company Overview</h4>
          <p className="text-sm text-gray-700 dark:text-gray-300">{kit.company_overview}</p>
        </div>
        <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Role Overview</h4>
          <p className="text-sm text-gray-700 dark:text-gray-300">{kit.role_overview}</p>
        </div>
      </div>

      {/* Responsibilities */}
      {kit.responsibilities.length > 0 && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Key Responsibilities</h4>
          <div className="space-y-2">
            {kit.responsibilities.map((resp, index) => (
              <div key={index} className="flex items-start space-x-2">
                <CheckCircle2 className="w-4 h-4 text-green-600 dark:text-green-400 mt-0.5" />
                <p className="text-sm text-gray-700 dark:text-gray-300">{resp}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Technical Topics */}
      {kit.technical_topics.length > 0 && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Technical Topics</h4>
          <div className="space-y-2">
            {kit.technical_topics.map((topic, index) => (
              <div key={index} className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-gray-900 dark:text-gray-100">{topic.topic}</span>
                  <span className="px-2 py-1 text-xs bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 rounded-full">
                    {topic.priority}
                  </span>
                </div>
                {topic.resources.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Resources:</p>
                    <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                      {topic.resources.map((resource, idx) => (
                        <li key={idx} className="flex items-start">
                          <span className="mr-2">•</span>
                          <span>{resource}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Behavioral Questions */}
      {kit.behavioral_questions.length > 0 && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Behavioral Questions</h4>
          <div className="space-y-3">
            {kit.behavioral_questions.slice(0, 5).map((q, index) => (
              <div key={index} className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                <div className="flex items-center justify-between mb-2">
                  <p className="font-medium text-gray-900 dark:text-gray-100">{q.question}</p>
                  <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300 rounded-full">
                    {q.priority}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  <strong>STAR Suggestion:</strong> {q.star_suggestion}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Study Plans */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
          <div className="flex items-center space-x-2 mb-3">
            <Clock className="w-4 h-4 text-green-600 dark:text-green-400" />
            <h4 className="font-medium text-gray-900 dark:text-gray-100">90-Min Plan</h4>
          </div>
          <div className="space-y-2">
            {kit.study_plan_90min.slice(0, 4).map((item, index) => (
              <div key={index} className="text-sm">
                <p className="font-medium text-gray-700 dark:text-gray-300">{item.time}</p>
                <p className="text-gray-600 dark:text-gray-400">{item.task}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="flex items-center space-x-2 mb-3">
            <Target className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            <h4 className="font-medium text-gray-900 dark:text-gray-100">3-Day Plan</h4>
          </div>
          <div className="space-y-2">
            {kit.study_plan_3day.slice(0, 3).map((day, index) => (
              <div key={index} className="text-sm">
                <p className="font-medium text-gray-700 dark:text-gray-300">{day.day}</p>
                <p className="text-gray-600 dark:text-gray-400">{day.focus}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
          <div className="flex items-center space-x-2 mb-3">
            <BookOpen className="w-4 h-4 text-purple-600 dark:text-purple-400" />
            <h4 className="font-medium text-gray-900 dark:text-gray-100">7-Day Plan</h4>
          </div>
          <div className="space-y-2">
            {kit.study_plan_7day.slice(0, 3).map((day, index) => (
              <div key={index} className="text-sm">
                <p className="font-medium text-gray-700 dark:text-gray-300">{day.day}</p>
                <p className="text-gray-600 dark:text-gray-400">{day.focus}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Questions to Ask */}
      {kit.questions_to_ask.length > 0 && (
        <div className="mt-6">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Questions to Ask the Interviewer</h4>
          <div className="space-y-2">
            {kit.questions_to_ask.slice(0, 5).map((q, index) => (
              <div key={index} className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <p className="font-medium text-gray-900 dark:text-gray-100">{q.question}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Reason: {q.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
