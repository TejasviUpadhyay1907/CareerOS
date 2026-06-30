'use client';

import { Target, TrendingUp, AlertCircle, CheckCircle2 } from 'lucide-react';

interface MatchScoreProps {
  overallMatch: number;
  technicalMatch: number;
  experienceMatch: number;
  educationMatch: number;
  atsMatch: number;
  matchReasoning: {
    technical: string;
    experience: string;
    education: string;
    ats: string;
  };
}

export function MatchScore({
  overallMatch,
  technicalMatch,
  experienceMatch,
  educationMatch,
  atsMatch,
  matchReasoning,
}: MatchScoreProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400';
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 dark:bg-green-900/30';
    if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900/30';
    return 'bg-red-100 dark:bg-red-900/30';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />;
    if (score >= 60) return <AlertCircle className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />;
    return <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />;
  };

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-6">
        <Target className="w-6 h-6 text-blue-600 dark:text-blue-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Match Analysis
        </h3>
      </div>

      {/* Overall Match Score */}
      <div className="flex items-center justify-center mb-8">
        <div className="relative">
          <div className="w-32 h-32 rounded-full border-8 border-gray-200 dark:border-gray-700 flex items-center justify-center">
            <div className="text-center">
              <div className={`text-4xl font-bold ${getScoreColor(overallMatch)}`}>
                {overallMatch}%
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400">Overall</div>
            </div>
          </div>
          <div className="absolute -top-2 -right-2">
            {getScoreIcon(overallMatch)}
          </div>
        </div>
      </div>

      {/* Detailed Scores */}
      <div className="space-y-4">
        <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span className="font-medium text-gray-700 dark:text-gray-300">Technical</span>
            </div>
            <span className={`font-semibold ${getScoreColor(technicalMatch)}`}>
              {technicalMatch}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mb-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                technicalMatch >= 80
                  ? 'bg-green-500'
                  : technicalMatch >= 60
                  ? 'bg-yellow-500'
                  : 'bg-red-500'
              }`}
              style={{ width: `${technicalMatch}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{matchReasoning.technical}</p>
        </div>

        <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span className="font-medium text-gray-700 dark:text-gray-300">Experience</span>
            </div>
            <span className={`font-semibold ${getScoreColor(experienceMatch)}`}>
              {experienceMatch}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mb-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                experienceMatch >= 80
                  ? 'bg-green-500'
                  : experienceMatch >= 60
                  ? 'bg-yellow-500'
                  : 'bg-red-500'
              }`}
              style={{ width: `${experienceMatch}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{matchReasoning.experience}</p>
        </div>

        <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span className="font-medium text-gray-700 dark:text-gray-300">Education</span>
            </div>
            <span className={`font-semibold ${getScoreColor(educationMatch)}`}>
              {educationMatch}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mb-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                educationMatch >= 80
                  ? 'bg-green-500'
                  : educationMatch >= 60
                  ? 'bg-yellow-500'
                  : 'bg-red-500'
              }`}
              style={{ width: `${educationMatch}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{matchReasoning.education}</p>
        </div>

        <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <Target className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span className="font-medium text-gray-700 dark:text-gray-300">ATS Score</span>
            </div>
            <span className={`font-semibold ${getScoreColor(atsMatch)}`}>{atsMatch}%</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mb-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                atsMatch >= 80 ? 'bg-green-500' : atsMatch >= 60 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${atsMatch}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{matchReasoning.ats}</p>
        </div>
      </div>
    </div>
  );
}
