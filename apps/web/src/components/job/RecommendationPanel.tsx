'use client';

import { Lightbulb, CheckCircle2, AlertTriangle, BookOpen, Award, Target } from 'lucide-react';

interface RecommendationPanelProps {
  insights: {
    top_strengths: string[];
    biggest_weaknesses: string[];
    reasons_recruiter_may_reject: string[];
    reasons_recruiter_may_shortlist: string[];
    hidden_expectations: string[];
    resume_gaps: string[];
    experience_gaps: string[];
    suggested_resume_changes: string[];
    suggested_projects: string[];
    suggested_certifications: string[];
    suggested_technologies: string[];
    suggested_interview_topics: string[];
  };
}

export function RecommendationPanel({ insights }: RecommendationPanelProps) {
  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-6">
        <Lightbulb className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          AI Insights & Recommendations
        </h3>
      </div>

      <div className="space-y-6">
        {/* Strengths */}
        {insights.top_strengths.length > 0 && (
          <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />
              <h4 className="font-medium text-green-700 dark:text-green-400">Top Strengths</h4>
            </div>
            <ul className="space-y-2">
              {insights.top_strengths.map((strength, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-green-600 dark:text-green-400">•</span>
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Weaknesses */}
        {insights.biggest_weaknesses.length > 0 && (
          <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400" />
              <h4 className="font-medium text-red-700 dark:text-red-400">Areas for Improvement</h4>
            </div>
            <ul className="space-y-2">
              {insights.biggest_weaknesses.map((weakness, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-red-600 dark:text-red-400">•</span>
                  <span>{weakness}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Shortlist Reasons */}
        {insights.reasons_recruiter_may_shortlist.length > 0 && (
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <CheckCircle2 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <h4 className="font-medium text-blue-700 dark:text-blue-400">
                Why You Might Get Shortlisted
              </h4>
            </div>
            <ul className="space-y-2">
              {insights.reasons_recruiter_may_shortlist.map((reason, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-blue-600 dark:text-blue-400">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Rejection Reasons */}
        {insights.reasons_recruiter_may_reject.length > 0 && (
          <div className="p-4 bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <AlertTriangle className="w-5 h-5 text-orange-600 dark:text-orange-400" />
              <h4 className="font-medium text-orange-700 dark:text-orange-400">
                Potential Rejection Reasons
              </h4>
            </div>
            <ul className="space-y-2">
              {insights.reasons_recruiter_may_reject.map((reason, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-orange-600 dark:text-orange-400">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Hidden Expectations */}
        {insights.hidden_expectations.length > 0 && (
          <div className="p-4 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <Lightbulb className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              <h4 className="font-medium text-purple-700 dark:text-purple-400">Hidden Expectations</h4>
            </div>
            <ul className="space-y-2">
              {insights.hidden_expectations.map((expectation, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-purple-600 dark:text-purple-400">•</span>
                  <span>{expectation}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Resume Changes */}
        {insights.suggested_resume_changes.length > 0 && (
          <div className="p-4 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-700 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <BookOpen className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              <h4 className="font-medium text-gray-700 dark:text-gray-300">Suggested Resume Changes</h4>
            </div>
            <ul className="space-y-2">
              {insights.suggested_resume_changes.map((change, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-gray-600 dark:text-gray-400">•</span>
                  <span>{change}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Projects */}
        {insights.suggested_projects.length > 0 && (
          <div className="p-4 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <Target className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
              <h4 className="font-medium text-indigo-700 dark:text-indigo-400">Suggested Projects</h4>
            </div>
            <ul className="space-y-2">
              {insights.suggested_projects.map((project, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-indigo-600 dark:text-indigo-400">•</span>
                  <span>{project}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Certifications */}
        {insights.suggested_certifications.length > 0 && (
          <div className="p-4 bg-teal-50 dark:bg-teal-900/20 border border-teal-200 dark:border-teal-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <Award className="w-5 h-5 text-teal-600 dark:text-teal-400" />
              <h4 className="font-medium text-teal-700 dark:text-teal-400">
                Suggested Certifications
              </h4>
            </div>
            <ul className="space-y-2">
              {insights.suggested_certifications.map((cert, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-teal-600 dark:text-teal-400">•</span>
                  <span>{cert}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Technologies */}
        {insights.suggested_technologies.length > 0 && (
          <div className="p-4 bg-cyan-50 dark:bg-cyan-900/20 border border-cyan-200 dark:border-cyan-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <BookOpen className="w-5 h-5 text-cyan-600 dark:text-cyan-400" />
              <h4 className="font-medium text-cyan-700 dark:text-cyan-400">
                Technologies to Learn
              </h4>
            </div>
            <div className="flex flex-wrap gap-2">
              {insights.suggested_technologies.map((tech, index) => (
                <span
                  key={index}
                  className="px-3 py-1 text-sm bg-cyan-100 text-cyan-700 dark:bg-cyan-900 dark:text-cyan-300 rounded-full"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Interview Topics */}
        {insights.suggested_interview_topics.length > 0 && (
          <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <Target className="w-5 h-5 text-amber-600 dark:text-amber-400" />
              <h4 className="font-medium text-amber-700 dark:text-amber-400">
                Interview Topics to Prepare
              </h4>
            </div>
            <ul className="space-y-2">
              {insights.suggested_interview_topics.map((topic, index) => (
                <li key={index} className="text-sm text-gray-700 dark:text-gray-300 flex items-start">
                  <span className="mr-2 text-amber-600 dark:text-amber-400">•</span>
                  <span>{topic}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
